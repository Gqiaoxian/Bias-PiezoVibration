
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QGroupBox, QProgressBar
from PySide6.QtCore import Qt, QObject, Signal, QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from nptdms import TdmsFile
from DataProUtil import DataProcessUtil

class _TdmsChunkLoadWorker(QObject):
    progress = Signal(int)
    finished = Signal(object, object)
    error = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            with TdmsFile.open(self.file_path) as tdms_file:
                groups = tdms_file.groups()
                if not groups:
                    raise ValueError("TDMS has no groups")
                group = groups[0]
                channels = group.channels()
                if len(channels) < 2:
                    raise ValueError("TDMS group has <2 channels")

                group_name = group.name
                bias_name = channels[0].name
                v_name = channels[1].name

                total = 0
                try:
                    total = int(len(channels[0]))
                except Exception:
                    total = 0

                bias_parts = []
                v_parts = []
                read_len = 0
                last_pct = -1
                self.progress.emit(0)

                for chunk in tdms_file.data_chunks():
                    bias_chunk = chunk[group_name][bias_name][:]
                    v_chunk = chunk[group_name][v_name][:]
                    bias_parts.append(np.asarray(bias_chunk))
                    v_parts.append(np.asarray(v_chunk))
                    read_len += int(len(bias_chunk))
                    if total > 0:
                        pct = int(min(100, max(0, (read_len * 100) // total)))
                        if pct != last_pct:
                            self.progress.emit(pct)
                            last_pct = pct

                df_bias = np.concatenate(bias_parts) if bias_parts else np.asarray([])
                df_v = np.concatenate(v_parts) if v_parts else np.asarray([])
                self.progress.emit(100)
                self.finished.emit(df_bias, df_v)
        except Exception as e:
            self.error.emit(str(e))

class DebugWaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.setWindowTitle("Waveform Viewer (Right-drag: Pan, Scroll: Zoom)")
        self.resize(1000, 700)
        self.setup_ui()
        self.current_logG = None
        self.current_bias = None
        self._load_thread = None
        self._load_worker = None
        self._pending_file_path = None
        self._pending_keyPara = None
        self._apply_callback = None
        self._sample_rate_provider = None
        self._key_para_provider = None
        self._last_keyPara = {}
        self._user_xlim_set = False
        self._default_xlim_applied = False
        self._render_start = 0
        self._render_len = 20000
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Info Label
        self.info_label = QLabel("Status: Waiting for data...")
        layout.addWidget(self.info_label)

        self.load_progress = QProgressBar(self)
        self.load_progress.setRange(0, 100)
        self.load_progress.setValue(0)
        self.load_progress.setVisible(False)
        layout.addWidget(self.load_progress)

        self.ctrl_group = QGroupBox("View / Generic Cut", self)
        ctrl_layout = QGridLayout(self.ctrl_group)

        self.sample_rate_input = QLineEdit(self.ctrl_group)
        self.sample_rate_input.setPlaceholderText("Sample rate (Hz)")
        ctrl_layout.addWidget(QLabel("Sample Rate(Hz)"), 0, 0)
        ctrl_layout.addWidget(self.sample_rate_input, 0, 1)

        self.view_start_input = QLineEdit(self.ctrl_group)
        self.view_start_input.setText("0")
        self.view_start_input.setPlaceholderText("0")
        self.view_len_input = QLineEdit(self.ctrl_group)
        self.view_len_input.setText("20000")
        self.view_len_input.setPlaceholderText("20000")
        ctrl_layout.addWidget(QLabel("View Start(x)"), 0, 2)
        ctrl_layout.addWidget(self.view_start_input, 0, 3)
        ctrl_layout.addWidget(QLabel("View Length(x)"), 0, 4)
        ctrl_layout.addWidget(self.view_len_input, 0, 5)

        self.apply_view_button = QPushButton("Apply View", self.ctrl_group)
        self.apply_view_button.clicked.connect(self.apply_view_window)
        ctrl_layout.addWidget(self.apply_view_button, 0, 6)

        self.cut_len_input = QLineEdit(self.ctrl_group)
        self.cut_len_input.setPlaceholderText("Additional length (x points)")
        ctrl_layout.addWidget(QLabel("AddLen(x)"), 1, 0)
        ctrl_layout.addWidget(self.cut_len_input, 1, 1)

        self.threshold_input = QLineEdit(self.ctrl_group)
        self.threshold_input.setPlaceholderText("Bias threshold (V)")
        ctrl_layout.addWidget(QLabel("Threshold(V)"), 2, 0)
        ctrl_layout.addWidget(self.threshold_input, 2, 1)

        self.cut_offset_input = QLineEdit(self.ctrl_group)
        self.cut_offset_input.setPlaceholderText("Cut offset (x points)")
        ctrl_layout.addWidget(QLabel("Cut Offset(x)"), 2, 2)
        ctrl_layout.addWidget(self.cut_offset_input, 2, 3)

        self.confirm_button = QPushButton("Confirm -> Write AddLen(x)", self.ctrl_group)
        self.confirm_button.clicked.connect(self.confirm_write_params)
        ctrl_layout.addWidget(self.confirm_button, 1, 2, 1, 2)

        self.time_preview_label = QLabel("Time(ms): -", self.ctrl_group)
        ctrl_layout.addWidget(self.time_preview_label, 1, 4, 1, 3)

        layout.addWidget(self.ctrl_group)

        self.cut_len_input.textChanged.connect(self._update_time_preview)
        self.sample_rate_input.textChanged.connect(self._update_time_preview)
        
        # Canvas
        self.figure = Figure(constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        
        self.ax = self.figure.add_subplot(111)
        
        # Connect event handlers for mouse interaction
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        # Pan state variables
        self._panning = False
        self._pan_start_x = 0
        self._pan_start_xlim = (0, 1)

    def _update_time_preview(self):
        try:
            window_points = float(self.cut_len_input.text())
        except Exception:
            window_points = None
        try:
            sample_rate = float(self.sample_rate_input.text())
        except Exception:
            sample_rate = None
        if window_points is None or sample_rate is None or window_points <= 0 or sample_rate <= 0:
            self.time_preview_label.setText("Time(ms): -")
            return
        time_ms = window_points * 1000.0 / sample_rate
        self.time_preview_label.setText(f"Time(ms): {time_ms:.6f}".rstrip('0').rstrip('.'))
        
    def on_scroll(self, event):
        """Mouse wheel zoom (X-axis only)"""
        if event.xdata is None or self.current_logG is None: return
        
        # Determine scale factor
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            return
            
        # Get current limits
        cur_xlim = self.ax.get_xlim()
        cur_xrange = cur_xlim[1] - cur_xlim[0]
        
        # Calculate new range
        new_xrange = cur_xrange * scale_factor
        
        # Calculate new limits to keep mouse position stationary
        new_xmin = event.xdata - (event.xdata - cur_xlim[0]) * scale_factor
        new_xmax = new_xmin + new_xrange
        
        # Clamp to buffer bounds [render_start, render_start + render_len]
        start, end = self._get_render_window()
        buffer_n = end - start
        if new_xrange > buffer_n:
            new_xmin = start
            new_xmax = end
        else:
            if new_xmin < start:
                new_xmax += (start - new_xmin)
                new_xmin = start
            if new_xmax > end:
                new_xmin -= (new_xmax - end)
                new_xmax = end
                if new_xmin < start: new_xmin = start
        
        self.ax.set_xlim([new_xmin, new_xmax])
        self._user_xlim_set = True
        self._sync_view_inputs_from_axes()
        self.canvas.draw_idle()
        
    def on_press(self, event):
        """Right mouse button to start panning"""
        if event.button == 3:  # Right click
            self._panning = True
            self._pan_start_x = event.x
            self._pan_start_xlim = self.ax.get_xlim()
            
    def on_release(self, event):
        """Release right mouse button to stop panning"""
        if event.button == 3:
            self._panning = False
            self._user_xlim_set = True
            self._sync_view_inputs_from_axes()
            
    def on_motion(self, event):
        """Drag to pan (X-axis only)"""
        if self._panning and event.x is not None and self.current_logG is not None:
            # Calculate pixel delta
            dx_pix = event.x - self._pan_start_x
            
            # Convert to data delta
            bbox = self.ax.get_window_extent()
            if bbox.width == 0: return
            
            start_range = self._pan_start_xlim[1] - self._pan_start_xlim[0]
            dx_data = (dx_pix / bbox.width) * start_range
            
            # Apply shift (minus because dragging right moves view left)
            new_xmin = self._pan_start_xlim[0] - dx_data
            new_xmax = self._pan_start_xlim[1] - dx_data
            
            # Clamp to buffer bounds [render_start, render_start + render_len]
            start, end = self._get_render_window()
            if new_xmin < start:
                new_xmax += (start - new_xmin)
                new_xmin = start
            if new_xmax > end:
                new_xmin -= (new_xmax - end)
                new_xmax = end
                if new_xmin < start: new_xmin = start

            self.ax.set_xlim([new_xmin, new_xmax])
            self.canvas.draw_idle()

    def update_raw_data(self, file_path, keyPara=None):
        """
        加载并显示原始数据的 LogG 波形
        """
        self._pending_file_path = file_path
        self._pending_keyPara = keyPara or {}
        self._start_async_load()

    def _start_async_load(self):
        file_path = self._pending_file_path
        keyPara = self._pending_keyPara or {}
        if not file_path:
            return

        try:
            if self._load_thread is not None:
                self._load_thread.quit()
                self._load_thread.wait(50)
        except Exception:
            pass

        self.current_logG = None
        self.current_bias = None
        self._last_keyPara = dict(keyPara) if isinstance(keyPara, dict) else {}
        self.info_label.setText(f"Loading: {file_path}")
        self.load_progress.setValue(0)
        self.load_progress.setVisible(True)

        self._load_thread = QThread(self)
        self._load_worker = _TdmsChunkLoadWorker(file_path)
        self._load_worker.moveToThread(self._load_thread)
        self._load_thread.started.connect(self._load_worker.run)
        self._load_worker.progress.connect(self._on_load_progress)
        self._load_worker.finished.connect(self._on_load_finished)
        self._load_worker.error.connect(self._on_load_error)
        self._load_worker.finished.connect(self._load_thread.quit)
        self._load_worker.error.connect(self._load_thread.quit)
        self._load_thread.start()

    def _on_load_progress(self, pct):
        try:
            self.load_progress.setValue(int(pct))
        except Exception:
            pass

    def _on_load_error(self, msg):
        self.load_progress.setVisible(False)
        self.info_label.setText(f"Error loading file: {msg}")

    def _on_load_finished(self, df_bias, df_V):
        keyPara = self._pending_keyPara or {}
        try:
            if keyPara and keyPara.get('mode') == 'RE_Irregular_Vabration':
                df_V_temp = df_bias
                df_bias_temp = df_V
                df_V = df_V_temp
                df_bias = df_bias_temp

            if self._sample_rate_provider is not None:
                try:
                    sr = self._sample_rate_provider()
                    self.sample_rate_input.setText(f"{float(sr):.6f}".rstrip('0').rstrip('.'))
                except Exception:
                    pass
            elif keyPara is not None:
                sr = keyPara.get('sample_rate_lineEdit', None)
                if sr is not None:
                    try:
                        self.sample_rate_input.setText(f"{float(sr):.6f}".rstrip('0').rstrip('.'))
                    except Exception:
                        pass

            th = None
            if keyPara is not None:
                th = keyPara.get('threshold_lineEdit', None)
                if th is None:
                    th = keyPara.get('bias_trigger_threshold', None)
            if th is not None and not self.threshold_input.text().strip():
                try:
                    self.threshold_input.setText(f"{float(th):.6f}".rstrip('0').rstrip('.'))
                except Exception:
                    pass

            co = None
            if keyPara is not None:
                co = keyPara.get('cut_offset_lineEdit', None)
            if co is not None and not self.cut_offset_input.text().strip():
                try:
                    self.cut_offset_input.setText(f"{float(co):.6f}".rstrip('0').rstrip('.'))
                except Exception:
                    pass

            # 新增：预填 additional_length
            add_len = None
            if keyPara is not None:
                add_len = keyPara.get('additional_length_lineEdit', None)
            if add_len is not None and not self.cut_len_input.text().strip():
                try:
                    self.cut_len_input.setText(f"{int(float(add_len))}")
                except Exception:
                    pass

            v0 = keyPara.get('v0_lineEdit', 0.1)
            g0 = keyPara.get('g0_lineEdit', 12.9)
            a1 = keyPara.get('a1_lineEdit', 4.1422)
            b1 = keyPara.get('b1_lineEdit', -13.196)
            a2 = keyPara.get('a2_lineEdit', -4.1044)
            b2 = keyPara.get('b2_lineEdit', -13.135)
            self.current_logG = DataProcessUtil.log_G_trans(df_V, v0, g0, a1, b1, a2, b2)
            self.current_bias = df_bias

            # 优先读取 UI 中的 View Start 和 View Length，作为初始渲染范围
            try:
                self._render_start = int(float(self.view_start_input.text() or "0"))
            except Exception:
                self._render_start = 0
            try:
                self._render_len = int(float(self.view_len_input.text() or "20000"))
            except Exception:
                self._render_len = 20000
            
            if not self.view_start_input.text().strip():
                self.view_start_input.setText(str(self._render_start))
            if not self.view_len_input.text().strip():
                self.view_len_input.setText(str(self._render_len))

            self.load_progress.setVisible(False)
            self.plot_waveform()
            self.info_label.setText(f"Loaded: {self._pending_file_path} | Points: {len(self.current_logG)}")
            self._update_time_preview()
        except Exception as e:
            self.load_progress.setVisible(False)
            self.info_label.setText(f"Error loading file: {e}")

    def setApplyCallback(self, callback):
        self._apply_callback = callback

    def setSampleRateProvider(self, provider):
        self._sample_rate_provider = provider

    def setKeyParaProvider(self, provider):
        self._key_para_provider = provider

    def _get_key_para(self):
        if self._key_para_provider is not None:
            try:
                kp = self._key_para_provider()
                if isinstance(kp, dict):
                    return kp
            except Exception:
                pass
        return self._last_keyPara or {}

    def _sync_view_inputs_from_axes(self):
        # 按照指令要求，缩放和拖动不应修改 View Start/Length 输入框的值
        pass

    def apply_view_window(self):
        if self.current_logG is None:
            return
        try:
            start = int(float(self.view_start_input.text()))
        except Exception:
            start = 0
        try:
            length = int(float(self.view_len_input.text()))
        except Exception:
            length = 20000
        n = int(len(self.current_logG))
        start = max(0, min(start, max(0, n - 1)))
        length = max(1, length)
        self._render_start = start
        self._render_len = length
        self._user_xlim_set = False
        self._default_xlim_applied = True
        self.preview_cut()

    def _get_render_window(self):
        """
        获取当前要渲染的数据索引范围。
        由 apply_view_window 确定的 _render_start 和 _render_len 为准。
        """
        if self.current_logG is None:
            return 0, 0
        n = int(len(self.current_logG))
        
        start = max(0, min(int(self._render_start), n - 1))
        length = max(1, int(self._render_len))
        end = min(n, start + length)
        
        return int(start), int(end)

    def confirm_write_params(self):
        try:
            window_points = float(self.cut_len_input.text())
        except Exception:
            return
        try:
            sample_rate = float(self.sample_rate_input.text())
        except Exception:
            return
        if sample_rate <= 0 or window_points <= 0:
            return
        time_ms = window_points * 1000.0 / sample_rate
        self.time_preview_label.setText(f"Time(ms): {time_ms:.6f}".rstrip('0').rstrip('.'))
        if self._apply_callback is not None:
            threshold_val = None
            if self.threshold_input.text().strip():
                try:
                    threshold_val = float(self.threshold_input.text())
                except Exception:
                    threshold_val = None
            cut_offset_val = None
            if self.cut_offset_input.text().strip():
                try:
                    cut_offset_val = float(self.cut_offset_input.text())
                except Exception:
                    cut_offset_val = None
            self._apply_callback(window_points, sample_rate, threshold_val, cut_offset_val)

    def preview_cut(self):
        keyPara = self._get_key_para()
        self.visualize_cut(keyPara, preview_only=True)

    def visualize_cut(self, keyPara, preview_only=False):
        """
        根据当前参数在图上画出切分线和结果
        """
        if self.current_logG is None:
            self.info_label.setText("No data loaded.")
            return

        try:
            try:
                sample_rate = float(self.sample_rate_input.text())
            except Exception:
                sample_rate = float(keyPara.get('sample_rate_lineEdit', 10000) or 10000)

            # 优先使用调试面板自身的输入，如果没有则使用主面板的 additional_length_lineEdit
            try:
                if self.cut_len_input.text().strip():
                    addtional_len = float(self.cut_len_input.text())
                else:
                    addtional_len = float(keyPara.get('additional_length_lineEdit', 0))
            except Exception:
                addtional_len = 0

            # 通用切割不再依赖 time_val，直接传 0 或从 keyPara 获取
            time_val = keyPara.get('time_lineEdit', 0)

            level_th = None
            if self.threshold_input.text().strip():
                try:
                    level_th = float(self.threshold_input.text())
                except Exception:
                    level_th = None
            if level_th is None:
                level_th = keyPara.get('threshold_lineEdit', None)
                if level_th is None:
                    level_th = keyPara.get('bias_trigger_threshold', None)

            cut_offset = None
            if self.cut_offset_input.text().strip():
                try:
                    cut_offset = float(self.cut_offset_input.text())
                except Exception:
                    cut_offset = None
            if cut_offset is None:
                cut_offset = keyPara.get('cut_offset_lineEdit', 0)

            data_s_e = DataProcessUtil.find_bias_trigger_points(
                self.current_bias,
                sample_rate,
                time_val,
                additional_length=addtional_len,
                level_threshold=level_th,
                cut_offset=cut_offset,
            )
            filtered_data_s_e = data_s_e
            
            # 3. 重新绘图并叠加标记
            self.plot_waveform()

            if self.current_bias is not None and level_th is not None:
                try:
                    bias = np.asarray(self.current_bias).astype(float).flatten()
                    n = int(bias.size)
                    baseline_n = min(n, max(50, int(round(n * 0.01))))
                    baseline = float(np.nanmedian(bias[:baseline_n])) if baseline_n > 0 else float(np.nanmedian(bias))
                    if hasattr(self, 'ax_bias') and self.ax_bias is not None and np.isfinite(baseline) and float(level_th) > 0:
                        self.ax_bias.axhline(y=baseline + float(level_th), color='orange', linestyle='--', linewidth=1, label='Threshold')
                        self.ax_bias.axhline(y=baseline - float(level_th), color='orange', linestyle='--', linewidth=1)
                except Exception:
                    pass
            
            if filtered_data_s_e is not None and len(filtered_data_s_e) > 0:
                if preview_only:
                    added_preview_label = False
                    for segment in filtered_data_s_e:
                        s = int(segment[0])
                        e = int(segment[1])
                        width = e - s
                        if width > 0:
                            ymin, ymax = self.ax.get_ylim()
                            label = 'Preview Cut' if not added_preview_label else None
                            rect = Rectangle((s, ymin), width, ymax - ymin,
                                             linewidth=1, edgecolor='orange', facecolor='yellow', alpha=0.25, label=label)
                            self.ax.add_patch(rect)
                            added_preview_label = True
                    self.info_label.setText(f"Preview: {len(filtered_data_s_e)} segments (Yellow)")
                    self.ax.legend(loc='upper right')
                    self.canvas.draw()
                    return

            if data_s_e is not None and len(data_s_e) > 0:
                valid_count = 0
                
                # 用于控制图例只添加一次
                added_valid_label = False
                
                for segment in data_s_e:
                    # 转换索引为整数
                    s = int(segment[0])
                    e = int(segment[1])
                    width = e - s
                    if width > 0:
                        ymin, ymax = self.ax.get_ylim()
                        label = 'Generic Cut' if not added_valid_label else None
                        rect = Rectangle((s, ymin), width, ymax - ymin, 
                                         linewidth=1, edgecolor='darkblue', facecolor='blue', alpha=0.25, label=label)
                        self.ax.add_patch(rect)
                        valid_count += 1
                        added_valid_label = True
                
                self.info_label.setText(f"Cut Result: {valid_count} Generic (Blue). Total: {len(data_s_e)}")
            else:
                self.info_label.setText(f"Cut Result: No valid segments found (Raw cuts: {len(data_s_e) if data_s_e else 0}).")
            
            self.ax.legend(loc='upper right')
            self.canvas.draw()
        except Exception as e:
            self.info_label.setText(f"Error during cut visualization: {e}")
            print(f"DebugWidget Cut Error: {e}")

    def plot_waveform(self):
        cur_xlim = None
        if self._user_xlim_set:
            try:
                cur_xlim = self.ax.get_xlim()
            except Exception:
                cur_xlim = None

        self.figure.clf()
        self.ax = self.figure.add_subplot(111)
        self.ax_bias = None

        if self.current_logG is not None:
            start, end = self._get_render_window()
            x = np.arange(start, end, dtype=int)
            y_log = np.asarray(self.current_logG[start:end]).astype(float).flatten()
            p1, = self.ax.plot(x, y_log, color='black', linewidth=0.5, label='LogG')
            self.ax.set_ylabel("Log(G/G0)", color='black')
            self.ax.set_xlabel("Index (x)")
            self.ax.tick_params(axis='y', labelcolor='black')
            self.ax.grid(True)

            if self.current_bias is not None:
                ax2 = self.ax.twinx()
                self.ax_bias = ax2
                y_bias = np.asarray(self.current_bias[start:end]).astype(float).flatten()
                p2, = ax2.plot(x, y_bias, color='blue', linewidth=0.5, label='Bias', alpha=0.6)
                ax2.set_ylabel("Bias Voltage (V)", color='blue')
                ax2.tick_params(axis='y', labelcolor='blue')

                lines = [p1, p2]
                self.ax.legend(lines, [l.get_label() for l in lines], loc='upper right')
            else:
                self.ax.legend(loc='upper right')

        if cur_xlim is not None:
            try:
                start, end = self._get_render_window()
                xmin, xmax = float(cur_xlim[0]), float(cur_xlim[1])
                xmin = max(float(start), min(xmin, float(end)))
                xmax = max(float(start), min(xmax, float(end)))
                if xmax <= xmin:
                    self.ax.set_xlim([start, end])
                else:
                    self.ax.set_xlim([xmin, xmax])
            except Exception:
                pass
        else:
            try:
                start, end = self._get_render_window()
                self.ax.set_xlim([start, end])
            except Exception:
                pass
            self._default_xlim_applied = True

        self._sync_view_inputs_from_axes()
        self.canvas.draw_idle()
