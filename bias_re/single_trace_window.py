from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QSizePolicy, QFileDialog
from PySide6.QtCore import Signal
import numpy as np
import os
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from ui.singletrace_ui import Ui_singletrace
from Myfigure import *


class SingleTraceWindow(QMainWindow):
    """
    简化的单条选择窗口：
    - 仅接受主程序传入的 `datasets`（list of dict，每条包含 'bias_segment' 和 'log_G' 等字段）
    - 提供单条浏览、选择、导出（NPZ/CSV）和发射所选完整 datasets 的功能
    """
    redrawRequested = Signal(list)

    def __init__(self, keyPara, parent=None):
        super().__init__(parent)
        self.ui = Ui_singletrace()
        self.ui.setupUi(self)
        self.keyPara = keyPara
        self.keyPara['single_window'] = True

        # 数据
        self.datasets = []
        self.valid_num = 0
        self.selected = set()
        self.cur_index = 0
        self.lastOpenPath = ''
        # 标记 datasets 来源：None / 'main' / 'npz' / 'user'
        self.datasets_source = None

        # matplotlib 画布
        self.canvas = FigureCanvas(Figure(constrained_layout=True))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.toolbar = MyNavigationToolbar(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax_right = self.ax.twinx()

        # 将画布放入 UI
        layout = QVBoxLayout(self.ui.widget)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        # 选择按钮
        self.select_btn = QPushButton("Toggle Select", self)
        layout.addWidget(self.select_btn)

        # 连接信号
        self.ui.rightpushButton.clicked.connect(self.next_trace)
        self.ui.leftpushButton.clicked.connect(self.prev_trace)
        self.select_btn.clicked.connect(self.toggle_select)
        self.ui.save_pushButton.clicked.connect(self.save_selected)
        self.ui.redrawpushButton.clicked.connect(self.request_redraw)
        self.ui.bias_checkBox.stateChanged.connect(lambda _: self.update_plot())
        self.ui.log_checkBox.stateChanged.connect(lambda _: self.update_plot())
        self.ui.peak_checkBox.stateChanged.connect(lambda _: self.update_plot())
        # 打开已保存的 npz 文件
        try:
            self.ui.open_pushButton.clicked.connect(self.open_npz)
        except Exception:
            pass
        # 全选复选框
        try:
            self.ui.Select_all_checkBox.stateChanged.connect(self.toggle_select_all)
        except Exception:
            pass

        # 只读显示
        self.ui.tracenum_lineEdit.setReadOnly(True)
        self.ui.chosennum_lineEdit.setReadOnly(True)
        self.ui.curindex_lineEdit.setReadOnly(True)

    def load_data(self, datasets, lastOpenPath=None, source='main'):
        """接收并保存完整的 datasets 列表（主程序传入）。
        参数 source 标记数据来源，方便决定是否允许主程序覆盖。"""
        self.datasets = list(datasets) if datasets is not None else []
        self.valid_num = len(self.datasets)
        if self.ui.Select_all_checkBox.isChecked():
            self.selected = set(range(self.valid_num))
        else:
            self.selected.clear()
        self.cur_index = 0
        self.ui.tracenum_lineEdit.setText(str(self.valid_num))
        self.ui.chosennum_lineEdit.setText(str(len(self.selected)))
        self.ui.curindex_lineEdit.setText(str(self.cur_index + 1))
        if lastOpenPath:
            self.lastOpenPath = lastOpenPath
        try:
            self.datasets_source = source
        except Exception:
            self.datasets_source = None
        self.update_plot()
        self._update_select_button_text()

    def try_update_from_main(self, datasets, lastOpenPath=''):
        """仅当当前窗口的数据来源允许被主程序覆盖（None 或 'main'）时，更新 datasets。
        返回 True 表示已更新，False 表示保留原数据。"""
        try:
            if self.datasets_source in (None, 'main'):
                self.load_data(datasets, lastOpenPath=lastOpenPath, source='main')
                return True
        except Exception:
            pass
        return False

    def _get_current_series(self):
        """返回当前索引对应的 (bias, logG) 两个 ndarray（保证是 ndarray），若不存在返回两个空 ndarray。"""
        # 如果当前索引无效，返回四个默认值以避免解包错误
        if not (0 <= self.cur_index < self.valid_num):
            return np.asarray([]), np.asarray([]), 0, 0
        ds = self.datasets[self.cur_index]
        # 兼容字段名：优先 'bias_segment' / 'log_G'，次选 'bias' / 'log'
        bias = np.asarray(ds.get('bias_segment') if ds.get('bias_segment') is not None else ds.get('bias', []))
        logG = np.asarray(ds.get('log_G') if ds.get('log_G') is not None else ds.get('log', []))

        # 计算 hover 起止，相对 data_s_e 起点；字段可能缺失，使用 try/except 以保证健壮性
        hover_s = 0
        hover_e = 0
        try:
            data_s_e = ds.get('data_s_e')
            hover_s_e = ds.get('hover_s_e')
            if data_s_e is not None and hover_s_e is not None:
                hover_s = int(hover_s_e[0]) - int(data_s_e[0])
                hover_e = int(hover_s_e[1]) - int(data_s_e[0])
        except Exception:
            hover_s = 0
            hover_e = 0

        return bias, logG, hover_s, hover_e

    def update_plot(self):
        bias, logG,hover_s,hover_e = self._get_current_series()

        plot_bias = self.ui.bias_checkBox.isChecked()
        plot_log = self.ui.log_checkBox.isChecked()
        plot_peak = self.ui.peak_checkBox.isChecked()
        if not plot_bias and not plot_log:
            QMessageBox.warning(self, "Warning", "Please select bias or Log(G/G0) to view")
            return

        # 清空画布
        self.ax.cla()
        self.ax_right.cla()

        # 确保都是 ndarray，再取长度以避免 "len() of unsized object" 错误
        bias = np.asarray(bias)
        logG = np.asarray(logG)

        # 决定 x 轴长度：优先以 logG 为准
        if plot_log and logG.size > 0:
            x = np.arange(logG.shape[0])
        else:
            x = np.arange(bias.shape[0])

        if plot_log and logG.size > 0:
            self.ax.plot(x, logG, color='tab:red', label='Log(G/G0)')
            self.ax.set_ylabel('Log(G/G0)', color='tab:red')
            self.ax.tick_params(axis='y', colors='tab:red')
        if plot_bias and bias.size > 0:
            self.ax_right.plot(x, bias, color='tab:blue', label='bias')
            self.ax_right.set_ylabel('Bias/RE', color='tab:blue')
            self.ax_right.tick_params(axis='y', colors='tab:blue')
            try:
                self.ax_right.yaxis.set_label_position('right')
                self.ax_right.yaxis.tick_right()
                self.ax_right.yaxis.label.set_padding(10)
            except Exception:
                pass
        if plot_peak and logG.size > 0:
            self.ax.axvline(hover_s, color='tab:green', alpha=0.3)
            self.ax.axvline(hover_e, color='tab:orange', alpha=0.3)
        self.canvas.draw_idle()
        self.ui.curindex_lineEdit.setText(str(self.cur_index + 1))
        self.ui.chosennum_lineEdit.setText(str(len(self.selected)))
        self._update_select_button_text()

    def next_trace(self):
        if self.cur_index + 1 < self.valid_num:
            self.cur_index += 1
            self.update_plot()

    def prev_trace(self):
        if self.cur_index - 1 >= 0:
            self.cur_index -= 1
            self.update_plot()

    def toggle_select(self):
        if self.cur_index in self.selected:
            self.selected.remove(self.cur_index)
        else:
            self.selected.add(self.cur_index)
        self.ui.chosennum_lineEdit.setText(str(len(self.selected)))
        self._update_select_button_text()

    def toggle_select_all(self, state):
        """全选或取消全选：state 为 0/2。"""
        try:
            if state:
                self.selected = set(range(self.valid_num))
            else:
                self.selected.clear()
            self.ui.chosennum_lineEdit.setText(str(len(self.selected)))
            self._update_select_button_text()
        except Exception:
            pass

    def _update_select_button_text(self):
        if self.cur_index in self.selected:
            self.select_btn.setText("Selected")
        else:
            self.select_btn.setText("Toggle Select")

    def save_selected(self):
        if len(self.selected) == 0:
            QMessageBox.warning(self, "Warning", "No traces selected to save")
            return

        folder = QFileDialog.getExistingDirectory(self, "Select folder to save", self.lastOpenPath)
        if not folder:
            return
        self.ui.save_pushButton.setEnabled(False)
        selected_indices = sorted(list(self.selected))
        selected_datasets = [self.datasets[i] for i in selected_indices]
        timestamp = time.time()
            # 转换为本地时间
        local_time = time.localtime(timestamp)
        # 格式化输出
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
        # NPZ 导出
        if self.ui.npzButton.isChecked():
            save_path = os.path.join(folder,f'selected_single_{formatted_time}')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            else:
                QMessageBox.warning(self, "Warning", f"selected_single_{formatted_time} folder already exists, please select another folder")
            save_path = os.path.join(save_path, 'selected_datasets.npz')
            # 收集各字段，使用 object dtype 保存不同长度
            data_s_e_list = [ds.get('data_s_e', None) for ds in selected_datasets]
            hover_list = [ds.get('hover_s_e', None) for ds in selected_datasets]
            log_G_peak = [ds.get('log_G_peak', None) for ds in selected_datasets]
            log_G_trough = [ds.get('log_G_trough', None) for ds in selected_datasets]
            bias_list = [np.asarray(ds.get('bias_segment') if ds.get('bias_segment') is not None else ds.get('bias', [])) for ds in selected_datasets]
            log_list = [np.asarray(ds.get('log_G') if ds.get('log_G') is not None else ds.get('log', [])) for ds in selected_datasets]
            # peaks_list = [ds.get('peaks', None) for ds in selected_datasets]
            # troughs_list = [ds.get('troughs', None) for ds in selected_datasets]

            np.savez_compressed(save_path,
                                data_s_e=np.array(data_s_e_list, dtype=object),
                                hover_s_e=np.array(hover_list, dtype=object),
                                log_G_peak=np.array(log_G_peak, dtype=object),
                                log_G_trough=np.array(log_G_trough, dtype=object),
                                bias=np.array(bias_list, dtype=object),
                                logG=np.array(log_list, dtype=object))
            QMessageBox.information(self, "Info", f"Saved {len(selected_indices)} traces to {save_path}")
        else:
            out_dir = os.path.join(folder, f'selected_datasets_csv_{formatted_time}')
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            else:
                QMessageBox.warning(self, "Warning", f"selected_datasets_csv_{formatted_time} folder already exists, please select another folder")
            index_rows = []
            for i, ds in enumerate(selected_datasets):
                trace_idx = int(selected_indices[i])
                bias_arr = np.asarray(ds.get('bias_segment') if ds.get('bias_segment') is not None else ds.get('bias', []))
                log_arr = np.asarray(ds.get('log_G') if ds.get('log_G') is not None else ds.get('log', []))
                data_path = os.path.join(out_dir, f'trace_{trace_idx+1}_data.csv')
                # 将 bias/log 保存为两列（长度可能不一致，较短的用 NaN 填充）
                max_len = max(bias_arr.size if hasattr(bias_arr, 'size') else len(bias_arr),
                              log_arr.size if hasattr(log_arr, 'size') else len(log_arr))
                bias_pad = np.full(max_len, np.nan, dtype=object)
                log_pad = np.full(max_len, np.nan, dtype=object)
                if bias_arr.size > 0:
                    bias_pad[:bias_arr.size] = bias_arr
                if log_arr.size > 0:
                    log_pad[:log_arr.size] = log_arr
                pd.DataFrame({'bias': bias_pad, 'log': log_pad}).to_csv(data_path, index=False)

                meta = {
                    'trace': trace_idx,
                    'data_s_e': ds.get('data_s_e', None),
                    'hover_s_e': ds.get('hover_s_e', None),
                    # 'peaks': str(ds.get('peaks', None)),
                    # 'troughs': str(ds.get('troughs', None)),
                    'data_csv': os.path.basename(data_path)
                }
                index_rows.append(meta)

            index_df = pd.DataFrame(index_rows)
            index_df.to_csv(os.path.join(out_dir, 'index.csv'), index=False)
            QMessageBox.information(self, "Info", f"Saved {len(selected_indices)} traces to {out_dir}")
        self.ui.save_pushButton.setEnabled(True)

    def request_redraw(self):
        """发射所选的完整 datasets 列表（每项为 dict）。"""
        selected_indices = sorted(list(self.selected))
        selected_datasets = [self.datasets[i] for i in selected_indices]
        try:
            self.datasets_source = 'user'
        except Exception:
            pass
        self.redrawRequested.emit(selected_datasets)

    def open_npz(self):
        """打开一个之前保存的 npz，转换成 datasets 格式并加载显示，同时触发主窗口重绘。"""
        path, _ = QFileDialog.getOpenFileName(self, 'Open NPZ', self.lastOpenPath or os.path.expanduser('~'), 'NPZ files (*.npz)')
        if not path:
            return
        try:
            arr = np.load(path, allow_pickle=True)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open file:\n{e}')
            return

        # 读取数组字段，按长度构建 datasets
        # 支持 keys: data_s_e, hover_s_e, segment_events, bias, logG
        bias_list = arr['bias'] if 'bias' in arr else (arr['bias_segment'] if 'bias_segment' in arr else None)
        log_list = arr['logG'] if 'logG' in arr else (arr['log'] if 'log' in arr else None)
        n = 0
        if bias_list is not None:
            n = len(bias_list)
        elif log_list is not None:
            n = len(log_list)
        else:
            QMessageBox.critical(self, 'Error', 'NPZ does not contain bias or log arrays')
            return

        datasets = []
        for i in range(n):
            ds = {}
            if 'data_s_e' in arr:
                ds['data_s_e'] = arr['data_s_e'][i]
            if 'hover_s_e' in arr:
                ds['hover_s_e'] = arr['hover_s_e'][i]
            if 'log_G_peak' in arr:
                ds['log_G_peak'] = arr['log_G_peak'][i]
            if 'log_G_trough' in arr:
                ds['log_G_trough'] = arr['log_G_trough'][i]

            # bias/log 可能为 object 数组，取元素并保证为 ndarray
            if bias_list is not None:
                ds['bias_segment'] = np.asarray(bias_list[i]) if bias_list[i] is not None else np.asarray([])
            if log_list is not None:
                ds['log_G'] = np.asarray(log_list[i]) if log_list[i] is not None else np.asarray([])

            datasets.append(ds)

        # 记录路径并加载
        self.lastOpenPath = os.path.dirname(path)
        self.load_data(datasets, lastOpenPath=self.lastOpenPath, source='npz')
        # 默认选择所有并发出 redraw
        self.selected = set(range(len(datasets)))
        self.ui.chosennum_lineEdit.setText(str(len(self.selected)))
        self._update_select_button_text()
        self.ui.Select_all_checkBox.setChecked(True)
        try:
            self.datasets_source = 'npz'
        except Exception:
            pass
        self.redrawRequested.emit(datasets)

    def closeEvent(self, event):
        """Override close: 默认隐藏窗口以便再次打开。
        当需要程序退出时，可设置 `self._force_close = True` 来允许真正关闭。
        """
        try:
            if getattr(self, '_force_close', False):
                # 允许真正关闭
                try:
                    event.accept()
                except Exception:
                    pass
            else:
                # 默认行为：隐藏并忽略关闭事件
                try:
                    self.hide()
                    event.ignore()
                except Exception:
                    try:
                        event.accept()
                    except Exception:
                        pass
        except Exception:
            try:
                event.accept()
            except Exception:
                pass
