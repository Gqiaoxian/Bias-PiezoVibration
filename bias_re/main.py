from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy, QProgressDialog
from PySide6.QtCore import Qt, QThread, QMetaObject, QTimer,QPropertyAnimation, QEasingCurve
import sys
import os
import math
import time
from multiprocessing import freeze_support
from scipy.signal import find_peaks
import configparser
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from zdDataAnalysis import DataAnalysisModel
from ui.vibration_ui import Ui_Vibratewidget
from ui.UI_MAINWINDOW_ui import Ui_BasicanalysisWindow
from ui.DebugWidget import DebugWaveformWidget
from DrawDataLoad import getAggregateDrawData
from saveworker import SaveWorker
from single_trace_window import SingleTraceWindow



from gangLogger.myLog import MyLog
from gangUtils.generalUtils import GeneralUtils
from myAboutWidget import QmyAbout
from Myfigure import *
from AnalysisConst import *

class BiasVibrationAnalysis(QMainWindow):
    logger = MyLog("BiasVibrationAnalysis", BASEDIR)
    def __init__(self,parent=None):
        super(BiasVibrationAnalysis,self).__init__(parent)
        self.ui = Ui_BasicanalysisWindow()
        self.ui.setupUi(self)
        self.keyPara = {}
        self.init_set()
        self.init_widget()


    def init_set(self):
        self.keyPara["viSaveData_Statue"] = False  # 此参数标志是否可以进行数据保存的工作，应当在得到绘图数据之后设置为True，并且在每点击一次run之后设置为False
        self.keyPara["Data_Save_Path"] = BASEDIR
        self.lastOpenPath = BASEDIR
        self.keyPara['single_draw'] = True  # 此参数标志是否是重画，重画无需在重新绘制单条
        self.keyPara['run_data'] = False
        # 退出标志位，按下退出按钮后设为 True，用于阻止后续绘图回调执行
        self.is_quit = False


    def init_widget(self):
        self.add_textBrowser_str("*" * 18 + "Welcome" + "*" * 18, showtime=False)
        logMsg = "Please load the data file first."
        self.add_textBrowser_str(logMsg)
        self.add_statusBar_str(logMsg)
        # self.initSaveDir()
#------------------------------------------------------设置参数-----------------------------------------------------------
        #选择不同分析数据模式
        self.ui.wave_select_comboBox.addItems(["Bias_Square_Vabration", "Bias_Sine_Vabration","Bias_Irregular_Vabration","RE_Irregular_Vabration"])
        
        
        
        # 添加绘画窗口
        self.vibration_ui = Ui_Vibratewidget()
        self.vibration_widget = QWidget()
        self.vibration_ui.setupUi(self.vibration_widget)
        self.ui.draw_stackedWidget.addWidget(self.vibration_widget)
        self.ui.draw_stackedWidget.setCurrentWidget(self.vibration_widget)
        
        # 颜色映射选择
        self.ui.color_2d_comboBox.addItems(["jet","rainbow","viridis","inferno","plasma","magma","YlOrRd","YlGnBu","GnBu"])
        # 添加画布
        layout = QVBoxLayout(self.vibration_ui.widget_2d)
        self.vib_2dcanvas = FigureCanvas(Figure(constrained_layout=True))
        self.vib_2dcanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vib_2dcanvas.updateGeometry()
        self.vib_2dtoolbar = MyNavigationToolbar(self.vib_2dcanvas)
        layout.addWidget(self.vib_2dcanvas)
        layout.addWidget(self.vib_2dtoolbar)
        layout = QVBoxLayout(self.vibration_ui.widget_1d)
        self.vib_1dcanvas = FigureCanvas(Figure(constrained_layout=True))
        self.vib_1dcanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vib_1dcanvas.updateGeometry()
        self.vib_1dtoolbar = MyNavigationToolbar(self.vib_1dcanvas)
        layout.addWidget(self.vib_1dcanvas)
        layout.addWidget(self.vib_1dtoolbar)
        self.singlecanvas = []
        
        # 按钮事件绑定设置
         # 加载数据
        self.ui.open_pushButton.clicked.connect(self.loadData)
         # 运行按钮
        self.ui.run_pushButton.clicked.connect(self.VibRunProcess)
        self.ui.view_pushButton.clicked.connect(self.openViewDialog)
        self.ui.run_pushButton.setEnabled(False) # 得加载数据
        self.ui.redraw_pushButton.clicked.connect(self.BtnRedrawClicked)
        
        self.ui.redraw_pushButton.setEnabled(False)
        self.ui.save_pushButton.setEnabled(False)
        self.logger.debug("The initial configuration is complete.")
        
        self.ui.quit_pushButton.clicked.connect(self.QuitPushButtonClicked)
        self.ui.about_pushButton.clicked.connect(self.showAbout)
        
        self.ui.save_pushButton.clicked.connect(self.VibActSaveData)
        self.initlabeltip()
        
        self.debugWidget = None
        self._view_dialog_file = None

        from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit
        self.use_generic_bias_cut_checkBox = QCheckBox("Use Generic Bias Cut", self.ui.cutPara_groupBox)
        self.use_generic_bias_cut_checkBox.setChecked(False)
        try:
            self.ui.horizontalLayout_12.insertWidget(1, self.use_generic_bias_cut_checkBox)
        except Exception:
            try:
                self.ui.horizontalLayout_12.addWidget(self.use_generic_bias_cut_checkBox)
            except Exception:
                pass
        self.cut_offset_label = QLabel("Cut Offset(x)", self.ui.cutPara_groupBox)
        try:
            self.cut_offset_label.setFont(self.ui.threlabel.font())
        except Exception:
            pass
        self.cut_offset_lineEdit = QLineEdit(self.ui.cutPara_groupBox)
        self.cut_offset_lineEdit.setObjectName("cut_offset_lineEdit")
        self.cut_offset_lineEdit.setToolTip("偏压切分起始点偏移量\n偏压切分用跳变那点作为起点\n但可用这个参数往前调节起点")
        try:
            self.cut_offset_lineEdit.setMinimumSize(self.ui.threshold_lineEdit.minimumSize())
            self.cut_offset_lineEdit.setMaximumSize(self.ui.threshold_lineEdit.maximumSize())
            self.cut_offset_lineEdit.setFont(self.ui.threshold_lineEdit.font())
        except Exception:
            pass
        self.cut_offset_lineEdit.setText("0")
        try:
            self.ui.gridLayout_10.addWidget(self.cut_offset_label, 2, 0, 1, 1)
            self.ui.gridLayout_10.addWidget(self.cut_offset_lineEdit, 2, 1, 1, 1)
        except Exception:
            pass

        self.ui.wave_select_comboBox.currentIndexChanged.connect(self._syncGenericCutCheckbox)
        self.use_generic_bias_cut_checkBox.toggled.connect(self._syncGenericCutExtraControls)
        self.ui.singleselect_pushButton.setEnabled(True)
        self.ui.singleselect_pushButton.clicked.connect(self.open_single_trace_window)
        self._syncGenericCutCheckbox()
        self.checkConfig()

    def showAbout(self):
        self.aboutWidget = QmyAbout()
        self.aboutWidget.show()
    def initlabeltip(self):
        self.ui.highcond_lineEdit.setToolTip("电导切分时电导上限")
        self.ui.lowcond_lineEdit.setToolTip("电导切分时电导下限")
        self.ui.additional_length_lineEdit.setToolTip("单条长度，对于电导切分小于这个长度的会被淘汰\n选择电导切分的话长度设置不要大于绝大多数单条\n对于偏压切分\n这个长度可以长一点没事\n用预览界面设置可提前查看切分效果")
        self.ui.time_lineEdit.setToolTip("悬停时间")
        self.ui.sample_rate_lineEdit.setToolTip("采样率")
        self.ui.square_frequence_lineEdit.setToolTip("方波频率")
        self.ui.sine_frequence_lineEdit_sine.setToolTip("正弦波频率")
        self.ui.threshold_lineEdit.setToolTip("偏压切分的阈值\n设置小一点\n不要大于振幅")
        self.ui.binsx_2d_lineEdit.setToolTip("绘制二维直方图，x轴的分箱数")
        self.ui.binsy_2d_lineEdit.setToolTip("绘制二维直方图，y轴的分箱数")
        self.ui.gmax_2d_lineEdit.setToolTip("绘制二维直方图和一维直方图，电导的最大值，单位log(G/G0)")
        self.ui.gmin_2d_lineEdit.setToolTip("绘制二维直方图和一维直方图，电导的最小值，单位log(G/G0)")
        self.ui.xmin_2d_lineEdit.setToolTip("绘制二维直方图，x轴的最小值")
        self.ui.xmax_2d_lineEdit.setToolTip("绘制二维直方图，x轴的最大值")
        self.ui.bins_1d_lineEdit.setToolTip("绘制一维直方图，电导分箱数")
        self.ui.cmin_2d_lineEdit.setToolTip("绘制二维直方图，所有计数小于的bin将不会显示\n色条映射最小值")
        self.ui.colormax_2d_lineEdit.setToolTip("绘制二维直方图，颜色映射条的最大值")
        self.ui.color_2d_comboBox.setToolTip("绘制二维直方图，颜色映射方案")



#---------------------------------------------------配置文件处理----------------------------------------------------------------
    def checkConfig(self):
        """
        检查配置文件
        """
        configPath = os.path.join(BASEDIR, "config.ini")
        self.add_textBrowser_str(configPath, showtime=False)
        if os.path.exists(configPath):
            dlgTitle = "Info"
            strInfo = "Config file detected. Load it??"
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(dlgTitle)
            msg_box.setText(strInfo)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint )
            reply = msg_box.exec()
            if reply == QMessageBox.Yes:
                self.getLastPara()
    def getLastPara(self):
        """
        加载程序同路径下保存好的历史参数并设置，
        :return:
        """
        try:
            config = configparser.ConfigParser()
            configPath = os.path.join(BASEDIR, "config.ini")
            config.read(configPath, encoding='utf-8')
            section_name = "PANEL_PARA"

            le_obj_list = []
            LINEEDIT_WIDGET_NEED_LIST = [self.ui.cutPara_groupBox, self.ui.draw_groupbox,self.ui.BasicPara_groupbox]

            for wdt in LINEEDIT_WIDGET_NEED_LIST:
                le_obj_list.extend(self.getSameWidget(wdt, QLineEdit))
            for obj in le_obj_list:
                name = obj.objectName()
                if config.has_option(section_name, name):
                    obj.setText(config.get(section_name, name))
            # obj_list_manual = [self.ui.savedir_lineEdit]
            # for obj in obj_list_manual:
            #     obj.setText(config.get(section_name, obj.objectName()))
            logMsg = "History parameters have been loaded"
            self.addLogMsgWithBar(logMsg)
        except Exception as e:
            errMsg = f"GTE OLD PARA ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
#---------------------------------------------------错误信息处理----------------------------------------------------------------
    def addErrorMsgWithBox(self, errMsg):
        self.logger.error(errMsg)
        QMessageBox.warning(self, "Warning", errMsg)
        self.add_statusBar_str(errMsg)
        self.add_textBrowser_str(errMsg)

    def addErrorMsgNoBox(self, errMsg):
        self.logger.error(errMsg)
        self.add_statusBar_str(errMsg)
        self.add_textBrowser_str(errMsg)

    def add_textBrowser_str(self, content_str, showtime=True):
        """
        在textBrowser中添加字符串
        :param content_str: 字符串
        :param showtime: 是否添加时间，默认true
        :return: 无返回值
        """
        try:
            if showtime:
                current_time = GeneralUtils.getCurrentTime()
                self.ui.textBrowser.append("[" + current_time + "]  " + content_str)
            else:
                self.ui.textBrowser.append(content_str)
        except Exception as e:
            errMsg = f"TEXT BROWSER ERROR:{e}"
            self.logger.error(errMsg)

    def addLogMsgWithBar(self, logMsg):
        self.logger.debug(logMsg)
        self.add_statusBar_str(logMsg)
        self.add_textBrowser_str(logMsg)

    def add_textBrowser_list(self, content_list, showtime=True):
        """
        在textBrowser中添加list
        :param content_list: 字符串列表
        :param showtime: 是否添加时间
        :return: 无返回值
        """
        try:
            if showtime:
                current_time = GeneralUtils.getCurrentTime()
                self.ui.textBrowser.append(current_time)
                for content in content_list:
                    content = content.split("/")[-1]
                    self.ui.textBrowser.append("-- " + content)
            else:
                for content in content_list:
                    content = content.split("/")[-1]
                    self.ui.textBrowser.append("-- " + content)
        except Exception as e:
            errMsg = f"TEXT BROWSER LIST ERROR:{e}"
            self.logger.error(errMsg)

    def add_statusBar_str(self, content_str):
        """
        状态栏添加文字
        :param content_str:字符串
        :return:无
        """
        try:
            self.ui.statusbar.showMessage(":) " + content_str)
        except Exception as e:
            errMsg = f"STATUSBAR ERROR{e}"
            self.logger.error(errMsg)
#---------------------------------------------------数据分析----------------------------------------------------------------
    # 加载数据
    def loadData(self):
            """
            文件加载
            :return:
            """
            try:
                dlg_title = "Select multiple file(s) " 
                filt = "TDMS Files(*.tdms);"  # 文件过滤器
                
                load_state = False
                while not load_state:
                    file_list, filt_used = QFileDialog.getOpenFileNames(self, dlg_title, self.lastOpenPath, filt)
                    load_state = True
                    if len(file_list) == 0:
                        warning_content = "Please select at least one file!"
                        load_state = False
                    
                    if not load_state:
                        result = QMessageBox.warning(self, "Warning", warning_content,
                                                    QMessageBox.Ok | QMessageBox.Cancel,
                                                    QMessageBox.Ok)
                        if result == QMessageBox.Cancel:
                            break
                        else:
                            continue
                    # 检查文件类型
                    # if filt_used== "TDMS Files(*.tdms)":
                    self.keyPara["FILE_TYPE"] = "tdms"
                    # 读取
                    self.lastOpenPath = os.path.dirname(file_list[0])
                    self.keyPara['FILE_PATHS'] = file_list
                    self.keyPara['mode'] = self.ui.wave_select_comboBox.currentText()
                    # 加载文件成功之后，应当对运行按钮进行释放
                    self.ui.run_pushButton.setEnabled(True)
                    self.add_textBrowser_str(f"{len(file_list)} {self.keyPara['mode']} files have been loaded:")
                    self.add_textBrowser_list(file_list)
                    self.add_textBrowser_str("*" * 45, showtime=False)
                    self.add_statusBar_str("File loading completed.")
                    self.logger.debug("File loading completed.")
                    
                    if len(file_list) > 0:
                        self._view_dialog_file = file_list[0]
                        if self.debugWidget is not None:
                            self.debugWidget.update_raw_data(self._view_dialog_file, self.getPanelPara())
                        
            except Exception as e:
                errMsg = f"DATA FILE LOAD ERROR:{e}"
                self.addErrorMsgWithBox(errMsg)
    def getSameWidget(self, widgetName, activeXName):
        """
        获取某个 widget 中同类型的控件
        :param widgetName: widget名，传入的是ui中的某个widget名
        :param activeXName: 控件类型，传入的是对象
        :return: 寻找到的对象集合(List)
        """
        return widgetName.findChildren(activeXName)
    def getPanelPara(self):
            """
            run之后，需要进行面板的参数采集
            :return:
            """
            keyPara = {}
            try:
                keyPara["ColorMap"] = self.ui.color_2d_comboBox.currentText()

                leObjList = []
                LINEEDIT_WIDGET_NEED_LIST = [self.ui.cutPara_groupBox, self.ui.draw_groupbox,self.ui.BasicPara_groupbox]
                for wdt in LINEEDIT_WIDGET_NEED_LIST:
                    leObjList.extend(self.getSameWidget(wdt, QLineEdit))
                for obj in leObjList:
                    keyPara[obj.objectName()] = float(obj.text())
            except Exception as e:
                errMsg = f"GTE PANEL PARA ERROR:{e}"
                self.addErrorMsgWithBox(errMsg)
                return None
            else:
                return keyPara
    
    def VibRunProcess(self):
        try:
            # 进度条初始化
            try:
                self.ui.progressBar.setMinimum(0)
                self.ui.progressBar.setMaximum(100)
                self.ui.progressBar.setValue(0)
            except Exception:
                self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar initialization failed.")
            # 每次开始新运行时重置退出标志
            self.is_quit = False
            self.ui.run_pushButton.setEnabled(False)  # 这里需要注意的是点击一次run 控件之后，应当设置未为不可选，
            self.ui.save_pushButton.setEnabled(False)
            self.ui.redraw_pushButton.setEnabled(False)
            self.keyPara["viSaveData_Statue"] = False

            keyPara = self.getPanelPara()
            keyPara['mode'] = self.ui.wave_select_comboBox.currentText()
            keyPara['single_draw'] = True
            keyPara['run_data'] = True
            keyPara['use_generic_bias_cut'] = bool(getattr(self, 'use_generic_bias_cut_checkBox', None) and self.use_generic_bias_cut_checkBox.isChecked())
            if keyPara is None:
                return
            else:
                self.keyPara.update(keyPara)
                self.logger.debug(f"vibration:Parameters are updated before running. Parameter list:{self.keyPara}")
                
                if getattr(self, 'debugWidget', None) is not None:
                    self.debugWidget.visualize_cut(self.keyPara)
                
                self.dataThread = QThread()
                self.dataAnalysis = DataAnalysisModel(self.keyPara)
                try:
                    self.ui.progressBar.setValue(10)
                except Exception:
                    self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
                
                self.dataAnalysis.runEnd.connect(lambda: self.stopThread(self.dataThread))
                self.dataAnalysis.runEnd.connect(self._on_data_run_end)
                
                self.dataAnalysis.moveToThread(self.dataThread)
                # Use a wrapper so we can prevent Run() execution if user requested quit
                self.dataThread.started.connect(self._on_dataThread_started)
                self.dataThread.finished.connect(self.DrawPre)

                logMsg = f"{self.keyPara['mode']}:Data calculation..."
                self.addLogMsgWithBar(logMsg)

                self.dataThread.start()
                self.logger.debug(
                    f"{self.keyPara['mode']}:Start the data calculation thread--{self.dataThread.currentThread()},Now state:{self.dataThread.isRunning()}")
        except Exception as e:
            errMsg = f"{self.keyPara['mode']}:RUN ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
            self.ui.progressBar.setValue(0)
    def _on_dataThread_started(self):
            if getattr(self, 'is_quit', False):
                self.addLogMsgWithBar("Start suppressed because user requested quit.")
                # ensure thread is not left running
                try:
                    if hasattr(self, 'dataThread') and self.dataThread.isRunning():
                        self.stopThread(self.dataThread)
                except Exception:
                    pass
                return
            # schedule Run() to be executed in the worker thread
            try:
                QMetaObject.invokeMethod(self.dataAnalysis, "Run", Qt.QueuedConnection)
            except Exception as e:
                self.addErrorMsgNoBox(f"Failed to invoke Run(): {e}")
    def _on_data_run_end(self):
        # 停止定时器并把进度设为完成
        try:
            self.ui.progressBar.setValue(50)
        except Exception:
            self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
    def DrawPre(self):
        if getattr(self, 'is_quit', False):
            self.addLogMsgWithBar(f"{self.keyPara['mode']}:Drawing skipped because process was terminated.")
            return
        self.logger.debug(f"{self.keyPara['mode']}:The computing process exits safely and begins computing drawing data")
        self.datasets = self.dataAnalysis.datasets
        try:
            self.cond_axis_corr_x,self.cond_axis_corr_y,self.log_G_peak,self.log_G_trough,self.valid_num,statue = getAggregateDrawData(self.keyPara,self.datasets)
            try:
                self.ui.progressBar.setValue(60)
            except Exception:
                self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
        except Exception as e:
            errMsg = f"{self.keyPara['mode']}:The parallel computing draw data aggregation error:{e}"
            self.addErrorMsgWithBox(errMsg)
            try:
                self.ui.progressBar.setValue(0)
            except Exception:
                self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
            self.ui.run_pushButton.setEnabled(True)
        else:
            if not statue:
                errMsg = f"{self.keyPara['mode']}:No valid drawing data, please adjust data"
                self.addErrorMsgWithBox(errMsg)
                try:
                    self.ui.progressBar.setValue(0)
                except Exception:
                    self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
                self.ui.run_pushButton.setEnabled(True)
                return
            else:
                # self.addLogMsgWithBar(f"Bias_Square_Vabration:All trace: {self.valid_num_vi}.")
                self.addLogMsgWithBar(f"{self.keyPara['mode']}:All trace: {self.valid_num}.")
                logMsg = f"{self.keyPara['mode']}:Start drawing..."
                self.addLogMsgWithBar(logMsg)
                try:
                    self.ui.progressBar.setValue(80)
                except Exception:
                    self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
                try:
                    self.VibDraw()
                except Exception as e:
                    self.ui.progressBar.setValue(0)
                    errMsg = f"{self.keyPara['mode']}:DRAW ERROR:{e}"
                    self.addErrorMsgWithBox(errMsg)
                else:
                    self.ui.redraw_pushButton.setEnabled(True)
        finally:
            self.ui.run_pushButton.setEnabled(True)
            try:
                self.ui.progressBar.setValue(100)
            except Exception:
                self.addLogMsgWithBar(f"{self.keyPara['mode']}:progressbar set value failed.")
    def VibDraw(self):
        if self.keyPara['mode'] == 'Bias_Square_Vabration' or self.keyPara['mode'] == 'Bias_Irregular_Vabration' or self.keyPara['mode'] == 'Bias_Sine_Vabration' or self.keyPara['mode'] == 'RE_Irregular_Vabration':
            # piezoamp = self.keyPara['piezo_amplitude_lineEdit']
            binsx = int(self.keyPara['binsx_2d_lineEdit'])  
            binsy = int(self.keyPara['binsy_2d_lineEdit']) 
            cmin = int(self.keyPara['cmin_2d_lineEdit']) 
            vmax = int(self.keyPara['colormax_2d_lineEdit']) if (int(self.keyPara['colormax_2d_lineEdit'])) != 0 else None
            xmin_2d = float(self.keyPara['xmin_2d_lineEdit']) if (float(self.keyPara['xmin_2d_lineEdit'])) != -10 else None
            xmax_2d = float(self.keyPara['xmax_2d_lineEdit']) if (float(self.keyPara['xmax_2d_lineEdit'])) != -10 else None
            dbins1 = int(self.keyPara['bins_1d_lineEdit'])
            gmax = self.keyPara.get('gmax_2d_lineEdit', 0)
            gmin = self.keyPara.get('gmin_2d_lineEdit', -6)

            x_arr = np.asarray(self.cond_axis_corr_x, dtype=float)
            y_arr = np.asarray(self.cond_axis_corr_y, dtype=float)

            if x_arr.size == 0 or y_arr.size == 0:
                raise ValueError("Empty drawing data for 2D histogram")

            try:
                gmin = float(gmin) if gmin is not None else None
            except Exception:
                gmin = None
            try:
                gmax = float(gmax) if gmax is not None else None
            except Exception:
                gmax = None

            y_min = float(np.nanmin(y_arr))
            y_max = float(np.nanmax(y_arr))
            if gmin is None or not np.isfinite(gmin):
                gmin = y_min
            if gmax is None or not np.isfinite(gmax):
                gmax = y_max
            if gmin == gmax:
                gmin = gmin - 1.0
                gmax = gmax + 1.0
            if gmin >= gmax:
                raise ValueError("Invalid g range: gmin must be < gmax")

            if xmin_2d is not None and xmax_2d is not None:
                if not np.isfinite(xmin_2d) or not np.isfinite(xmax_2d):
                    raise ValueError("Invalid x range from panel")
                if xmin_2d >= xmax_2d:
                    raise ValueError("Invalid x range: xmin must be < xmax")
                x_range = [xmin_2d, xmax_2d]
            else:
                x_min = float(np.nanmin(x_arr))
                x_max = float(np.nanmax(x_arr))
                if not np.isfinite(x_min) or not np.isfinite(x_max):
                    raise ValueError("Invalid x data for 2D histogram")
                if x_min == x_max:
                    x_range = [x_min - 1.0, x_max + 1.0]
                else:
                    x_range = [x_min, x_max]
            xmin_2d, xmax_2d = float(x_range[0]), float(x_range[1])

            range_2d = [x_range, [gmin, gmax]]
            # 清空并创建两个子图
            self.vib_2dcanvas.figure.clf()
            ax1 = self.vib_2dcanvas.figure.add_subplot()
            # 2D直方图
            H,xedges,yedges = np.histogram2d(self.cond_axis_corr_x, self.cond_axis_corr_y, bins=[binsx, binsy],range=[x_range, [gmin, gmax]])
            h = ax1.hist2d(self.cond_axis_corr_x, self.cond_axis_corr_y, cmin=cmin, vmax=vmax,
                        bins=[binsx, binsy],range=[x_range, [gmin, gmax]],
                        cmap=self.keyPara.get('ColorMap', 'rainbow'))
            # self.addLogMsgWithBar(f"{H.shape}: {H}.")
            
            # 保存二维直方图矩阵（counts）和边界
            try:
                # H = h[0]
                # xedges = h[1]
                # yedges = h[2]
                # 保留为整数矩阵，便于保存
                self.d2H = H
                self.d2_xedges = xedges
                self.d2_yedges = yedges
            except Exception:
                # 兼容性保护
                self.d2H = None
                self.d2_xedges = None
                self.d2_yedges = None
            ax1.set_xlabel("Time (ms)")
            ax1.set_ylabel("Log(G/G0)")
            ax1.set_ylim(gmin,gmax)
            if xmin_2d is not None and xmax_2d is not None:
                ax1.set_xlim(xmin_2d, xmax_2d)
            self.vib_2dcanvas.figure.colorbar(h[3], ax=ax1)
            self.vib_1dcanvas.figure.clf()
            self.peakH = None
            self.troughH = None
            self.peak_bins = None
            self.trough_bins = None
            if self.keyPara['mode'] == 'Bias_Square_Vabration' or self.keyPara['mode'] == 'Bias_Sine_Vabration':
                ax2 = self.vib_1dcanvas.figure.add_subplot()
                # 1D概率分布 — 先计算原始计数以便保存，再归一化用于绘图
                raw_peak_counts, peak_bins = np.histogram(self.log_G_peak, bins=dbins1,range=[gmin, gmax])
                raw_trough_counts, trough_bins = np.histogram(self.log_G_trough, bins=dbins1,range=[gmin, gmax])
                # 保存原始计数（整数）和 bin 边界
                self.peakH = raw_peak_counts.astype(int)
                self.troughH = raw_trough_counts.astype(int)
                self.peak_bins = peak_bins
                self.trough_bins = trough_bins

                # 归一化用于绘图（防止除以零）
                peak_counts_plot = raw_peak_counts.astype(float)
                trough_counts_plot = raw_trough_counts.astype(float)
                if peak_counts_plot.sum() > 0:
                    peak_counts_plot = peak_counts_plot / peak_counts_plot.sum()
                if trough_counts_plot.sum() > 0:
                    trough_counts_plot = trough_counts_plot / trough_counts_plot.sum()

                ax2.barh((peak_bins[:-1] + peak_bins[1:]) / 2, peak_counts_plot, height=(peak_bins[1] - peak_bins[0]),
                        color='red', alpha=0.5, edgecolor='none', label='Peak')
                ax2.barh((trough_bins[:-1] + trough_bins[1:]) / 2, trough_counts_plot, height=(trough_bins[1] - trough_bins[0]),
                color='blue', alpha=0.5, edgecolor='none', label='Trough')
                max_val = max(peak_counts_plot.max(), trough_counts_plot.max())
                if max_val < 1e-2:
                    ax2.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
                ax2.set_xlabel('Counts')
                ax2.set_ylim(gmin,gmax)
                ax2.legend(['Peak','Trough'])
                ax2.grid(True)
            self.vib_2dcanvas.draw()
            self.vib_1dcanvas.draw()
            self.vib_2dcanvas.flush_events()
            self.vib_1dcanvas.flush_events()
            # 绘图结束
            logMsg = f"{self.keyPara['mode']}:Draw finished"
            self.addLogMsgWithBar(logMsg)
            self.keyPara["viSaveData_Statue"] = True  # 这个true放在这里的目的是只要绘图完成一遍，就说明产生了新数据，可以保存
            self.ui.save_pushButton.setEnabled(True)
            self.ui.run_pushButton.setEnabled(True)
            # 如果 single_trace_window 已存在且允许主程序覆盖（None 或 'main'），则更新其 datasets
        if self.keyPara['run_data'] :
            if hasattr(self, 'single_trace_window') and self.single_trace_window is not None:
                self.single_trace_window.load_data(datasets=getattr(self, 'datasets', []), lastOpenPath=getattr(self, 'lastOpenPath', ''), source='main')
                self.keyPara['run_data'] = False
                self.ui.run_pushButton.setEnabled(True)
        try:
            if hasattr(self, 'single_trace_window') and self.single_trace_window is not None:
                try:
                    _ = getattr(self, 'datasets', None)
                    # 调用窗口内部的 try_update_from_main，只有在窗口允许覆盖时才会更新
                    try:
                        updated = self.single_trace_window.try_update_from_main(getattr(self, 'datasets', []), getattr(self, 'lastOpenPath', ''))
                    except Exception:
                        updated = False
                except Exception:
                    pass
        except Exception:
            pass
#----------------------------------------------------重画按钮-------------------------------------------
    def BtnRedrawClicked(self):
        try:
            keyPara = self.getPanelPara()
            if keyPara is None:
                return
            else:
                self.keyPara.update(keyPara)
                self.logger.debug(f"Parameters are updated before running. Parameter list:{self.keyPara}")
                self.ui.save_pushButton.setEnabled(False)
                self.ui.run_pushButton.setEnabled(False)
                self.VibDraw()
        except Exception as e:
            errMsg = f"REDRAW ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
            self.ui.run_pushButton.setEnabled(True)
#---------------------------------------------------单条筛选窗口-----------------------------------------------------
    def open_single_trace_window(self):
        keyPara = self.getPanelPara()
        keyPara['mode'] = self.ui.wave_select_comboBox.currentText()
        keyPara['single_draw'] = True
        if keyPara is None:
            return
        else:
            self.keyPara.update(keyPara)
        try:
            # 如果已经打开则激活并恢复（处理最小化）
            if hasattr(self, 'single_trace_window') and self.single_trace_window is not None:
                w = self.single_trace_window
                try:
                    src = getattr(w, 'datasets_source', None)
                    # 如果主程序已有数据且窗口当前显示的是 NPZ 或 用户自定义数据，询问是否用主数据替换
                    if getattr(self, 'datasets', None) and src in ('npz', 'user'):
                        reply = QMessageBox.question(self, "Replace data?",
                                                     "Main has new run results. Replace current single-window data with main results?",
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            try:
                                w.load_data(datasets=getattr(self, 'datasets', []), lastOpenPath=getattr(self, 'lastOpenPath', ''), source='main')
                            except TypeError:
                                try:
                                    w.load_data(getattr(self, 'datasets', []))
                                except Exception:
                                    pass
                    else:
                        # 对于最初为空或已是 main 数据的窗口，尝试保持或刷新为主数据
                        if src in (None, 'main') and getattr(self, 'datasets', None):
                            try:
                                w.load_data(datasets=getattr(self, 'datasets', []), lastOpenPath=getattr(self, 'lastOpenPath', ''), source='main')
                            except TypeError:
                                try:
                                    w.load_data(getattr(self, 'datasets', []))
                                except Exception:
                                    pass

                    # 恢复并激活窗口
                    if w.isMinimized():
                        w.showNormal()
                    else:
                        w.show()
                    w.raise_()
                    w.activateWindow()
                except Exception:
                    try:
                        w.show()
                    except Exception:
                        pass
                return
            # 创建独立窗口（不以主窗口为 parent，避免随主窗口最小化）
            self.single_trace_window = SingleTraceWindow(self.keyPara, parent=None)
            # 如果窗口被真正删除，应在 destroyed 时清理引用
            try:
                self.single_trace_window.destroyed.connect(lambda _=None: setattr(self, 'single_trace_window', None))
            except Exception:
                pass
            # 连接重绘信号
            self.single_trace_window.redrawRequested.connect(self.on_single_redraw)

            # 如果已有运行产生的 datasets，则传入；否则传入空列表以显示空白画布
            datasets_to_load = []
            if hasattr(self, 'datasets') and getattr(self, 'datasets'):
                datasets_to_load = getattr(self, 'datasets')

            try:
                self.single_trace_window.load_data(datasets=datasets_to_load, lastOpenPath=getattr(self, 'lastOpenPath', ''))
            except TypeError:
                # 兼容老版本签名（如果没有 lastOpenPath 参数）
                try:
                    self.single_trace_window.load_data(datasets_to_load)
                except Exception:
                    pass

            # 显示窗口（窗口可能为空白，但可打开以便用户查看/操作）
            self.single_trace_window.show()
        except Exception as e:
            self.addErrorMsgWithBox(f"Open single trace window failed: {e}")

    def on_single_redraw(self, chosen_indices):
        """
        接收来自单条窗口的选择：支持两种输入格式。
        - 如果传入的是索引列表（int），保留原有行为。
        - 如果传入的是每条的完整 `datasets` 列表（dict），则直接使用 `getDrawData` 聚合并重绘主窗口。
        """
        keyPara = self.getPanelPara()
        self.keyPara["viSaveData_Statue"] = False
        keyPara['mode'] = self.ui.wave_select_comboBox.currentText()
        keyPara['single_draw'] = True
        if keyPara is None:
            return
        else:
            self.keyPara.update(keyPara)
        try:
            if not chosen_indices:
                self.addLogMsgWithBar("No trace chosen for redraw.")
                return

            # 如果传入的是 datasets（dict 列表），直接用 DrawDataLoad.getDrawData 生成绘图数据
            first = chosen_indices[0]
            if isinstance(first, dict):
                try:
                    cond_x, cond_y, log_G_peak, log_G_trough, valid_num, ok = getAggregateDrawData(self.keyPara,chosen_indices)
                except Exception as e:
                    self.addErrorMsgWithBox(f"Redraw:getDrawData failed: {e}")
                    return
                if not ok:
                    self.addLogMsgWithBar("No valid data from selected datasets.")
                    return

                self.cond_axis_corr_x = cond_x
                self.cond_axis_corr_y = cond_y
                self.log_G_peak = log_G_peak
                self.log_G_trough = log_G_trough

                # 调用绘图（使用选中的 trace 数量作为 valid_num，使绘制以新数据为基础）
                self.VibDraw()
                return

            # sampfrequency = float(self.keyPara['sample_frequence_lineEdit'])
            # piezoamp = float(self.keyPara.get('piezo_amplitude_lineEdit', 0))

            # # 根据模式提取 start/end
            # starts = []
            # ends = []
            # if self.ui.newmethod_checkBox.isChecked():
            #     for i in chosen_indices:
            #         s = int(self.hover_start[int(i)])
            #         e = int(self.hover_end[int(i)])
            #         starts.append(s)
            #         ends.append(e)
            #     log_arr = self.df_log
            #     piezo_arr = self.df_piezo
            # else:
            #     for i in chosen_indices:
            #         s = int(self.start_point_vi[int(i)])
            #         e = int(self.end_point_vi[int(i)])
            #         starts.append(s)
            #         ends.append(e)
            #     log_arr = self.df_logG_vi
            #     piezo_arr = self.df_piezo_vi

            # # 重新计算 cond_axis_x/y（简单按 trace 内时间起点为 0 拼接）
            # cond_axis_x = []
            # cond_axis_y = []
            # for s, e in zip(starts, ends):
            #     length = e - s
            #     for j in range(length):
            #         cond_axis_x.append(j / sampfrequency)
            #         cond_axis_y.append(float(log_arr[s + j]))

            # # 重新计算 1D 的 peak/trough（使用现有方法）
            # sel_start_arr = np.array(starts, dtype=int)
            # sel_end_arr = np.array(ends, dtype=int)
            # log_G_peak, log_G_trough = self.one_D_conductance_histogram_square_wave(log_arr, piezo_arr, sel_start_arr, sel_end_arr, piezoamp)

            # # 将计算结果设置到实例变量并重绘
            # self.cond_axis_corr_x = cond_axis_x
            # self.cond_axis_corr_y = cond_axis_y
            # self.log_G_peak = log_G_peak
            # self.log_G_trough = log_G_trough

            # # 调用绘图（使用选中的 trace 数量作为 valid_num，使绘制以新数据为基础）
            # self.Vibdraw(len(starts))
        except Exception as e:
            self.addErrorMsgWithBox(f"Redraw from single trace failed: {e}")
#----------------------------------------------------进程终止----------------------
    def QuitPushButtonClicked(self):
        # 非阻塞请求退出：设置标志并请求中断，不在主线程阻塞等待
        self.is_quit = True
        try:
            if hasattr(self, 'dataAnalysis'):
                if hasattr(self.dataAnalysis, 'request_stop'):
                    try:
                        self.dataAnalysis.request_stop()
                    except Exception:
                        setattr(self.dataAnalysis, 'is_quit', True)
                else:
                    setattr(self.dataAnalysis, 'is_quit', True)
        except Exception:
            pass

        if hasattr(self, 'dataThread') and self.dataThread.isRunning():
            try:
                # 请求中断，不会阻塞
                self.dataThread.requestInterruption()
            except Exception:
                pass

            # 用定时器异步检查线程是否退出，避免阻塞主线程
            try:
                if hasattr(self, '_quit_check_timer') and self._quit_check_timer.isActive():
                    self._quit_check_timer.stop()
                self._quit_check_timer = QTimer(self)
                self._quit_check_timer.setInterval(100)
                def _check():
                    if not self.dataThread.isRunning():
                        self._quit_check_timer.stop()
                        self._on_thread_stopped_after_quit()
                self._quit_check_timer.timeout.connect(_check)
                self._quit_check_timer.start()
            except Exception:
                pass

            self.addLogMsgWithBar("Data processing termination requested.")
            try:
                self.ui.progressBar.setValue(0)
            except Exception:
                pass
        else:
            self.addLogMsgWithBar("No running data thread to stop.")
            try:
                self.ui.progressBar.setValue(0)
            except Exception:
                pass

    def _on_thread_stopped_after_quit(self):
        # 线程真正退出后的 UI 清理（在主线程调用）
        try:
            self.ui.run_pushButton.setEnabled(True)
            self.ui.save_pushButton.setEnabled(False)
            self.ui.redraw_pushButton.setEnabled(False)
            self.addLogMsgWithBar("Data thread stopped.")
            self.ui.progressBar.setValue(0)
        except Exception:
            pass

    def stopThread(self, thread):
        """
        立即请求中断并返回（非阻塞）。尽量不要在主线程中循环等待线程退出。
        若必须等待短时间，请使用 QTimer 异步轮询或在调用方使用信号/槽处理后续清理。
        """
        try:
            try:
                thread.requestInterruption()
            except Exception:
                pass
            try:
                thread.quit()
            except Exception:
                pass
            # 不再在这里做长时间阻塞等待，避免卡死 UI
            self.logger.debug(f"Requested stop for thread {thread.currentThread()}")
        except Exception as e:
            self.addErrorMsgWithBox(f"PRECESS EXIT ERROR:{e}")
#--------------------------------------------------------保存数据--------------------------------------------
    def saveConfigPara(self,dir_path):
        """
        结束保存参数
        :return:
        """
        try:
            config = configparser.ConfigParser()
            config.optionxform = str  # 这一句相当的关键，因为config这个模块会把option自动的变为全小写，这个设置可以保持原样！
            section_name = "PANEL_PARA"
            config.add_section(section_name)
            le_obj_list = []
            LINEEDIT_WIDGET_NEED_LIST = [self.ui.cutPara_groupBox, self.ui.draw_groupbox,self.ui.BasicPara_groupbox]

            for wdt in LINEEDIT_WIDGET_NEED_LIST:
                le_obj_list.extend(self.getSameWidget(wdt, QLineEdit))
            for obj in le_obj_list:
                config.set(section_name, obj.objectName(), obj.text())
            # ========这一部分需要手动添加=====
            # obj_list_manual = [self.ui.savedir_lineEdit]
            # for obj in obj_list_manual:
            #     config.set(section_name, obj.objectName(), obj.text())
            configPath = os.path.join(dir_path, "config.ini")
            with open(configPath, mode="w", encoding="utf-8") as f:
                config.write(f)
            self.logger.debug("Parameters have been saved")
        except Exception as e:
            errMsg = f"PARA SAVE ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)

    def VibActSaveData(self):
            try:
                self.ui.run_pushButton.setEnabled(False)
                self.ui.save_pushButton.setEnabled(False)
                self.ui.redraw_pushButton.setEnabled(False)
                self.ui.quit_pushButton.setEnabled(False)
                self.ui.open_pushButton.setEnabled(False)
                logMsg = "Save data..."
                self.addLogMsgWithBar(logMsg)
                preCheck = self.savePreCheck()
                self.progressDialog = QProgressDialog("Saving data...", None, 0, 100, self)
                self.progressDialog.setWindowModality(Qt.ApplicationModal)
                self.progressDialog.setAutoClose(False)
                self.progressDialog.setCancelButton(None)
                self.progressDialog.setWindowTitle("Please wait")
                self.progressDialog.setMinimumDuration(0)
                self.progressDialog.show()
                self.progressDialog.setValue(0)
                QApplication.processEvents()
                time.sleep(1)
                self.progressDialog.setValue(10)
                if preCheck:
                    dataSavePath = self.keyPara["Data_Save_Path"]
                    self.VibsaveFig(dataSavePath)
                    self._save_data_thread = QThread()
                    self.save_data = SaveWorker(self.keyPara,dataSavePath,self.d2H,self.d2_xedges,self.d2_yedges,self.peak_bins,self.peakH,self.trough_bins)
                    self.save_data.moveToThread(self._save_data_thread)
                    # self.save_data.progress.connect(lambda v: self.progressDialog.setValue(int(v)))
                    self.save_data.save_run_end.connect(lambda: self.stopThread(self._save_data_thread))   
                    self._save_data_thread.started.connect(self.save_data.run)
                    self._save_data_thread.finished.connect(self.show_finished_save)
                    self._save_data_thread.start()
                else:
                    self.ui.run_pushButton.setEnabled(True)
                    self.ui.save_pushButton.setEnabled(True)
                    self.ui.redraw_pushButton.setEnabled(True)
                    self.ui.quit_pushButton.setEnabled(True)
                    self.ui.open_pushButton.setEnabled(True)
                    errMsg = "DATA SAVE STOP"
                    self.addErrorMsgWithBox(errMsg)
            except Exception as e:
                errMsg = f"DATA SAVE ERROR:{e}"
                self.addErrorMsgWithBox(errMsg)
    def show_finished_save(self):
        self.progressDialog.setValue(100)
        data_save_path = self.keyPara["Data_Save_Path"]
        self.saveConfigPara(data_save_path)
        self.progressDialog.close()
        logMsg = f"All data has been saved. Path:{data_save_path}"
        self.addLogMsgWithBar(logMsg)
        QMessageBox.information(self, "Info", logMsg)
        self.ui.run_pushButton.setEnabled(True)
        self.ui.save_pushButton.setEnabled(True)
        self.ui.redraw_pushButton.setEnabled(True)
        self.ui.quit_pushButton.setEnabled(True)
        self.ui.open_pushButton.setEnabled(True)
    def VibsaveFig(self, dataSavePath):
            """
            图片保存
            :param dataSavePath:
            :return:
            """
            imgPath = os.path.join(dataSavePath, "Images")
            GeneralUtils.creatFolder(dataSavePath, "Images")
            d2Path = os.path.join(imgPath, "2D.png")
            d1Path = os.path.join(imgPath, "1D.png")
            if self.keyPara['mode'] == 'Bias_Square_Vabration' or self.keyPara['mode'] == 'Bias_Sine_Vabration':
                self.vib_1dcanvas.figure.savefig(d1Path, dpi=100, bbox_inches='tight')
            # 2d 图都要保存
            self.vib_2dcanvas.figure.savefig(d2Path, dpi=100, bbox_inches='tight')

    def _syncGenericCutCheckbox(self):
        cb = getattr(self, 'use_generic_bias_cut_checkBox', None)
        if cb is None:
            return
        mode = self.ui.wave_select_comboBox.currentText()
        enable = mode in ('Bias_Square_Vabration', 'Bias_Sine_Vabration', 'Bias_Irregular_Vabration', 'RE_Irregular_Vabration')
        cb.setVisible(enable)
        cb.setEnabled(enable)
        if not enable:
            try:
                cb.setChecked(False)
            except Exception:
                pass
        self._syncGenericCutExtraControls()

    def _syncGenericCutExtraControls(self):
        cb = getattr(self, 'use_generic_bias_cut_checkBox', None)
        show = bool(cb is not None and cb.isVisible() and cb.isChecked())
        for w in (
            getattr(self.ui, 'threlabel', None),
            getattr(self.ui, 'threshold_lineEdit', None),
            getattr(self, 'cut_offset_label', None),
            getattr(self, 'cut_offset_lineEdit', None),
        ):
            if w is None:
                continue
            try:
                w.setVisible(show)
            except Exception:
                pass

    def openViewDialog(self):
        if getattr(self, 'debugWidget', None) is None:
            self.debugWidget = DebugWaveformWidget(parent=None)
            self.debugWidget.setApplyCallback(self.applyGenericCutWindowFromPoints)
            self.debugWidget.setSampleRateProvider(lambda: float(self.ui.sample_rate_lineEdit.text()))
            self.debugWidget.setKeyParaProvider(self._getViewDialogKeyPara)

        file_path = self._view_dialog_file
        if not file_path:
            if self.keyPara.get('FILE_PATHS'):
                file_path = self.keyPara['FILE_PATHS'][0]
                self._view_dialog_file = file_path
        if file_path:
            self.debugWidget.update_raw_data(file_path, self._getViewDialogKeyPara())
        self.debugWidget.show()
        self.debugWidget.raise_()
        self.debugWidget.activateWindow()

    def _getViewDialogKeyPara(self):
        panel_para = dict(self.keyPara) if isinstance(getattr(self, 'keyPara', None), dict) else {}
        ui_para = self.getPanelPara() or {}
        panel_para.update(ui_para)
        panel_para['mode'] = self.ui.wave_select_comboBox.currentText()
        panel_para['use_generic_bias_cut'] = bool(getattr(self, 'use_generic_bias_cut_checkBox', None) and self.use_generic_bias_cut_checkBox.isChecked())
        return panel_para

    def applyGenericCutWindowFromPoints(self, window_points, sample_rate, threshold_val=None, cut_offset_val=None):
        try:
            window_points = float(window_points)
            sample_rate = float(sample_rate)
        except Exception:
            return
        if sample_rate <= 0:
            return
        
        # 通用切割模式下，直接将点数写入 additional_length_lineEdit
        self.ui.additional_length_lineEdit.setText(f"{int(window_points)}")
        self.ui.sample_rate_lineEdit.setText(f"{sample_rate:.6f}".rstrip('0').rstrip('.'))
        if threshold_val is not None:
            try:
                threshold_val = float(threshold_val)
            except Exception:
                threshold_val = None
            if threshold_val is not None:
                try:
                    self.ui.threshold_lineEdit.setText(f"{threshold_val:.6f}".rstrip('0').rstrip('.'))
                except Exception:
                    pass
                self.keyPara['threshold_lineEdit'] = threshold_val
                self.keyPara['bias_trigger_threshold'] = threshold_val

        if cut_offset_val is not None:
            try:
                cut_offset_val = float(cut_offset_val)
            except Exception:
                cut_offset_val = None
            if cut_offset_val is not None:
                try:
                    if hasattr(self, 'cut_offset_lineEdit') and self.cut_offset_lineEdit is not None:
                        self.cut_offset_lineEdit.setText(f"{cut_offset_val:.6f}".rstrip('0').rstrip('.'))
                except Exception:
                    pass
                self.keyPara['cut_offset_lineEdit'] = cut_offset_val
    
    def savePreCheck(self):
        """
        数据保存之前的检查
        :return:
        """
        if not self.keyPara["viSaveData_Statue"]:
            errMsg = f"{self.ui.wave_select_comboBox.currentText()}:The data cannot be saved until the data processing is complete!"
            self.addErrorMsgWithBox(errMsg)
            return False
        
        try:
            title = "Choose the target folder, and a 'result' directory will be created under it."
            # cur_path = self.keyPara['Data_Save_Path']
            dir_selected = QFileDialog.getExistingDirectory(self, title, self.lastOpenPath, QFileDialog.ShowDirsOnly)
            if dir_selected == "":
                return False
            dlgTitle = "Folder name Settings"
            txtLabel = "Please enter the name of the folder to save"
            timestamp = time.time()
            # 转换为本地时间
            local_time = time.localtime(timestamp)
            # 格式化输出
            formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
            defaultName = f"{self.ui.wave_select_comboBox.currentText()}{formatted_time}"
            echoMode = QLineEdit.Normal
            saveDataDir = dir_selected
            flag = False
            while not flag:
                text, OK = QInputDialog.getText(self, dlgTitle, txtLabel, echoMode, defaultName)
                if OK:
                    savePath = os.path.join(saveDataDir, text)
                    IS_EXIST = os.path.exists(savePath)
                    if IS_EXIST:
                        errMsg = "The file name already exists or is invalid,Please re-enter"
                        self.addErrorMsgWithBox(errMsg)
                        continue
                    else:
                        flag = not flag
                        self.keyPara["Data_Save_Path"] = savePath
                        GeneralUtils.creatFolder(saveDataDir, text)  # 存储路径直接在这里创建
                else:
                    logMsg = "Unsave data"
                    self.addLogMsgWithBar(logMsg)
                    return False
            return True
        except Exception as e:
            self.addErrorMsgWithBox(f"folder create fail: {e}")
            return False
    def closeEvent(self, event):
        """
        重写窗口关闭函数，关闭前保存面板参数
        :param event: 无
        :return: 无
        """
        dlg_title = "Warning"
        str_info = "Sure to quit??"
        reply = QMessageBox.question(self, dlg_title, str_info,
                                     QMessageBox.Yes | QMessageBox.Cancel,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.saveConfigPara(BASEDIR)
            time.sleep(0.1)
            self.logger.debug("Program exits")
            # 在退出前，如果单条窗口存在，尝试强制关闭
            try:
                if hasattr(self, 'single_trace_window') and self.single_trace_window is not None:
                    try:
                        # 设置窗口允许强制关闭的标志并调用 close()
                        setattr(self.single_trace_window, '_force_close', True)
                        self.single_trace_window.close()
                    except Exception:
                        try:
                            self.single_trace_window.deleteLater()
                        except Exception:
                            pass
                    try:
                        self.single_trace_window = None
                    except Exception:
                        pass
            except Exception:
                pass
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)
    window = BiasVibrationAnalysis()
    window.show()
    sys.exit(app.exec())
