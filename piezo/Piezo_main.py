from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy
from PySide6.QtCore import Qt, QThread, QMetaObject
import sys
import os
import configparser
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import multiprocessing
from zdDataAnalysis import DataAnalysismodel
from ui.vibration_ui import Ui_Vibratewidget
from ui.piezo_calibration_ui import Ui_piezocalibration
from ui.UI_MAINWINDOW_ui import Ui_basicanalysiswindow
from ui.vibbutton_ui import Ui_vibbutton
from ui.pcabutton_ui import Ui_pcabutton
from ui.Cut_Para_ui import Ui_Form as Ui_CutParaForm
from ui.Piezo_Para_ui import Ui_Form as Ui_PiezoParaForm
from gangLogger.myLog import MyLog
from gangUtils.generalUtils import GeneralUtils
from myAboutWidget import QmyAbout
from Myfigure import *
from AnalysisConst import *
from DrawDataLoad import getDrawData
from single_trace_window import SingleTraceWindow

class VibrationAnalysis(QMainWindow):
    logger = MyLog("VibrationAnalysis", BASEDIR)
    def __init__(self,parent=None):
        super(VibrationAnalysis,self).__init__(parent)
        self.ui = Ui_basicanalysiswindow()
        self.ui.setupUi(self)
        self.keyPara = {}
        self.init_set()
        self.init_widget()


    def init_set(self):
        self.keyPara["viSaveData_Statue"] = False  # 此参数标志是否可以进行数据保存的工作，应当在得到绘图数据之后设置为True，并且在每点击一次run之后设置为False
        self.keyPara["pcaSaveData_Statue"] = False  
        self.keyPara["Data_Save_Path"] = BASEDIR
        self.lastOpenPath = BASEDIR
        self.keyPara['single_draw'] = False  # 此参数标志是否是重画，重画无需在重新绘制单条
        self.keyPara['single_window'] = False # 此标志用于确定单条的窗口是否可以显示
        # 退出标志位，按下退出按钮后设为 True，用于阻止后续绘图回调执行
        self.keyPara['run_data'] = False # 判断是否用主窗口运行的数据去覆盖单条软件筛选窗口
        self.is_quit = False


    def init_widget(self):
        self.add_textBrowser_str("*" * 18 + "Welcome" + "*" * 18, showtime=False)
        logMsg = "Please load the data file first."
        self.add_textBrowser_str(logMsg)
        self.add_statusBar_str(logMsg)
        # self.initSaveDir()
        self.vibbutton_ui = Ui_vibbutton()
        self.vibbuttonwidget =  QWidget()
        self.vibbutton_ui.setupUi(self.vibbuttonwidget)
        self.pcabutton_ui = Ui_pcabutton()
        self.pcabuttonwidget =  QWidget()
        self.pcabutton_ui.setupUi(self.pcabuttonwidget)
        self.ui.stackedWidget_button.addWidget(self.vibbuttonwidget)
        self.ui.stackedWidget_button.addWidget(self.pcabuttonwidget)
        self.ui.stackedWidget_button.setCurrentWidget(self.vibbuttonwidget)
        self.vibration_ui = Ui_Vibratewidget()
        self.vibration_widget = QWidget()
        self.vibration_ui.setupUi(self.vibration_widget)
        self.pcalibration_ui = Ui_piezocalibration()
        self.pcalibration_widget = QWidget()
        self.pcalibration_ui.setupUi(self.pcalibration_widget)
        # self.piezocalibrationWidget = PiezoCalibrationWidget()
        
        self.ui.stackedWidget.addWidget(self.vibration_widget)
        self.ui.stackedWidget.addWidget(self.pcalibration_widget)
        self.ui.stackedWidget.setCurrentWidget(self.vibration_widget)
        self.setup_parameter_pages()

        self.ui.comboBox.addItems(["vibration_square","vibration_sine","vibration_triangle","vibration_irregular" ,"piezo_calibration",])
        self.ui.comboBox.currentIndexChanged.connect(self.switchMode)
        self.ui.comboBox.setCurrentIndex(0)

        self.ui.color_comboBox.addItems(["rainbow","jet","viridis","inferno"])

        self.vibbutton_ui.open_pushButton.clicked.connect(self.loadData)
        self.pcabutton_ui.open_pushButton.clicked.connect(self.loadData)
        self.vibbutton_ui.run_pushButton.clicked.connect(self.VibRunProcess)
        self.pcabutton_ui.run_pushButton.clicked.connect(self.PcaRunProcess)
        self.vibbutton_ui.run_pushButton.setEnabled(False) # 得加载数据
        self.pcabutton_ui.run_pushButton.setEnabled(False)
        self.ui.redraw_pushButton.setEnabled(False)
        self.ui.singleFilter_pushButton.setEnabled(True)
        self.ui.singleFilter_pushButton.clicked.connect(self.open_single_trace_window)
        # self.vibration_ui.leftpushButton.clicked.connect(self.goto_prev_page)
        # self.vibration_ui.rightpushbotton.clicked.connect(self.goto_next_page)
        self.vibbutton_ui.save_pushButton.setEnabled(False)
        self.pcabutton_ui.save_pushButton.setEnabled(False)


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
        layout = QVBoxLayout(self.pcalibration_ui.widget)
        self.piezo_1dcanvas = FigureCanvas(Figure(constrained_layout=True))
        self.piezo_1dcanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.piezo_1dcanvas.updateGeometry()
        self.piezo_1dtoolbar = MyNavigationToolbar(self.piezo_1dcanvas)
        layout.addWidget(self.piezo_1dcanvas)
        layout.addWidget(self.piezo_1dtoolbar)
        self.singlecanvas = []
        self.ui.redraw_pushButton.clicked.connect(self.BtnRedrawClicked)

        self.logger.debug("The initial configuration is complete.")
        self.vibbutton_ui.save_pushButton.clicked.connect(self.VibActSaveData)
        self.pcabutton_ui.save_pushButton.clicked.connect(self.PcaActSaveData)
        self.ui.quit_pushButton.clicked.connect(self.QuitPushButtonClicked)
        
        self.ui.about_pushButton.clicked.connect(self.showAbout)
        # self.ui.newmethod_checkBox.setChecked(True)
        self.initlabeltip()
        self.checkConfig()

    def setup_parameter_pages(self):
        self.cut_para_ui = Ui_CutParaForm()
        self.cut_para_widget = QWidget()
        self.cut_para_ui.setupUi(self.cut_para_widget)

        self.piezo_para_ui = Ui_PiezoParaForm()
        self.piezo_para_widget = QWidget()
        self.piezo_para_ui.setupUi(self.piezo_para_widget)

        while self.ui.Para_stackedWidget.count() > 0:
            widget = self.ui.Para_stackedWidget.widget(0)
            self.ui.Para_stackedWidget.removeWidget(widget)
            widget.deleteLater()

        self.ui.Para_stackedWidget.addWidget(self.cut_para_widget)
        self.ui.Para_stackedWidget.addWidget(self.piezo_para_widget)
        self.cut_para_ui.range_open_checkBox.toggled.connect(self.toggle_cut_cond_range_visibility)
        self.toggle_cut_cond_range_visibility(self.cut_para_ui.range_open_checkBox.isChecked())
        self.update_parameter_page_for_mode(self.ui.comboBox.currentText())

    def toggle_cut_cond_range_visibility(self, checked):
        self.cut_para_ui.cond_range_groupBox.setVisible(bool(checked))

    def update_parameter_page_for_mode(self, mode):
        if mode == "piezo_calibration":
            self.ui.Para_stackedWidget.setCurrentWidget(self.piezo_para_widget)
        else:
            self.ui.Para_stackedWidget.setCurrentWidget(self.cut_para_widget)

    def _unique_widgets_by_object_name(self, widgets):
        result = []
        seen = set()
        for widget in widgets:
            name = widget.objectName()
            if not name or name in seen:
                continue
            seen.add(name)
            result.append(widget)
        return result

    def _get_common_basic_line_edits(self):
        result = []
        for widget in self.getSameWidget(self.ui.BasicPara_groupbox, QLineEdit):
            if not self.ui.Para_stackedWidget.isAncestorOf(widget):
                result.append(widget)
        return result

    def _get_current_parameter_line_edits(self):
        current_widget = self.ui.Para_stackedWidget.currentWidget()
        if current_widget is None:
            return []
        return self.getSameWidget(current_widget, QLineEdit)

    def _get_all_parameter_line_edits(self):
        line_edits = []
        if hasattr(self, "cut_para_widget"):
            line_edits.extend(self.getSameWidget(self.cut_para_widget, QLineEdit))
        if hasattr(self, "piezo_para_widget"):
            line_edits.extend(self.getSameWidget(self.piezo_para_widget, QLineEdit))
        return line_edits

    def _get_parameter_checkboxes(self):
        checkboxes = []
        if hasattr(self, "cut_para_ui"):
            checkboxes.append(self.cut_para_ui.range_open_checkBox)
        return checkboxes

    def set_progress_value(self, value):
        self.ui.progressBar.setValue(max(0, min(100, int(value))))

    def showAbout(self):
        self.aboutWidget = QmyAbout()
        self.aboutWidget.show()
    def QuitPushButtonClicked(self):
        # 设置退出标志并终止数据处理线程
        self.is_quit = True
        if hasattr(self, 'dataThread') and self.dataThread.isRunning():
            # 先设置标志，stopThread 会触发 finished 信号，VibdrawPre 会检查 is_quit 并跳过绘图
            self.stopThread(self.dataThread)
            if self.ui.comboBox.currentText() != "piezo_calibration":
                self.vibbutton_ui.run_pushButton.setEnabled(True)
            else:
                self.pcabutton_ui.run_pushButton.setEnabled(True)# 确保运行按钮可用
            self.addLogMsgWithBar("Data processing has been terminated by user.")



    # def initSaveDir(self):
    #     desktop_path = GeneralUtils.getDesktopPath()
    #     self.ui.savedir_lineEdit.setText(desktop_path)

    def initlabeltip(self):
        self.ui.hover_frequence_lineEdit.setToolTip("机械振荡频率，单位Hz")
        self.ui.sample_frequence_lineEdit.setToolTip("采样率，将采样点转化为时间")
        self.ui.time_lineEdit.setToolTip("悬停时间") # 时间label
        self.ui.binsx_lineEdit.setToolTip("绘制二维直方图，x轴的分箱数")
        self.ui.binsy_lineEdit.setToolTip("绘制二维直方图，y轴的分箱数")
        self.ui.G_max_lineEdit.setToolTip("绘制二维直方图和一维直方图，电导的最大值，单位log(G/G0)")
        self.ui.G_min_lineEdit.setToolTip("绘制二维直方图和一维直方图，电导的最小值，单位log(G/G0)")
        self.ui.x_2d_min_lineEdit.setToolTip("绘制二维直方图x轴最小值")
        self.ui.x_2d_max_lineEdit.setToolTip("绘制二维直方图x轴最大值")
        self.ui.d1bins_lineEdit.setToolTip("绘制波峰波谷一维直方图分箱数")
        self.ui.colormaplabel.setToolTip("配色设置")
        self.ui.cmin_lineEdit.setToolTip("绘制二维直方图，所有计数小于的bin将不会显示")
        self.ui.colormax_lineEdit.setToolTip("绘制二维直方图，颜色映射条的最大值")
        self.ui.xl_lineEdit.setToolTip("校正一维直方图x的左侧值") # 时间label
        self.ui.xh_lineEdit.setToolTip("校正一维直方图x的右侧值") # 时间label
        self.ui.pbins_lineEdit.setToolTip("校正一维直方图的分箱数")
        self.vibbutton_ui.run_pushButton.setToolTip("振荡数据分析")
        self.vibbutton_ui.save_pushButton.setToolTip("保存结果")
        self.vibbutton_ui.open_pushButton.setToolTip("打开振荡数据文件")
        self.ui.redraw_pushButton.setToolTip("重新绘制")
        self.ui.quit_pushButton.setToolTip("停止数据分析")
        self.ui.about_pushButton.setToolTip("关于")
        self.ui.singleFilter_pushButton.setToolTip("单条数据分析筛选")
        self.pcabutton_ui.run_pushButton.setToolTip("校正数据分析")
        self.pcabutton_ui.open_pushButton.setToolTip("打开校正数据文件")
        self.pcabutton_ui.save_pushButton.setToolTip("保存结果")
        self.cut_para_ui.hoveramplitude_lineEdit.setToolTip("机械振荡振幅")
        self.cut_para_ui.peaknum_lineEdit.setToolTip("波峰和波谷总数,\n设置为0时自动计算,计算公式:hover_frequency*time/1000*2\n如果实际的数量与计算的有+1或者-1的数量的出入，\n可以按实际填写\n否则波峰波谷统计会根据自动计算的波峰波谷数统计\n比如计算得到的总的波峰波谷数是4，实际为5，多出的最后那段波峰或波谷不统计\n如计算得到的为4，实际为3，,会把piezo最后下降那段统计进去")
        self.cut_para_ui.threshold_lineEdit.setToolTip("推荐值为0.1,0.01和0.001,\n在hoveramplitude_lineEdit<=0.001时使用0.01,\n在hoveramplitude_lineEdit<=0.0001时使用0.001\n这个值允许振荡的振幅在hoveramplitude*（1-threshold）~hoveramplitude*（1+threshold）之间波动，\n防止piezo振荡段带来的数据抖动，\n在无法分析数据时可以根据实际数据微调这个值\n不要设置太大，否则会把前面延迟的那一段统计进去")
        self.cut_para_ui.range_open_checkBox.setToolTip("是否开启电导范围校正")
        self.cut_para_ui.highcond_lineEdit.setToolTip("振荡段电导必须全部小于等于该值")
        self.cut_para_ui.lowcond_lineEdit.setToolTip("振荡段电导必须全部大于等于该值")
        self.cut_para_ui.length1dfit_lineEdit.setToolTip("每段波峰波谷统计的长度，\n只取中间部分不取两端，\n取[每段波峰中间-length1dfit/2-每段波谷中间+length1dfit/2]的电导值做一维波峰波谷统计")
        self.piezo_para_ui.piezo_highcond_lineEdit.setToolTip("切分单条时电导上限")
        self.piezo_para_ui.piezo_lowcond_lineEdit.setToolTip("切分单条时电导下限")
        self.piezo_para_ui.lenhigh_lineEdit.setToolTip("校正时电导上限")
        self.piezo_para_ui.lenlow_lineEdit.setToolTip("校正时电导下限")
        self.ui.V0_lineEdit.setToolTip("偏压值")



    def getPanelPara(self):
        """
        run之后，需要进行面板的参数采集
        :return:
        """
        keyPara = {}
        try:
            keyPara["ColorMap"] = self.ui.color_comboBox.currentText()

            leObjList = []
            leObjList.extend(self._get_common_basic_line_edits())
            leObjList.extend(self._get_current_parameter_line_edits())
            leObjList.extend(self.getSameWidget(self.ui.draw_groupbox, QLineEdit))
            leObjList = self._unique_widgets_by_object_name(leObjList)
            for obj in leObjList:
                keyPara[obj.objectName()] = float(obj.text())
        except Exception as e:
            errMsg = f"GTE PANEL PARA ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
            return None
        else:
            return keyPara
        
    def checkConfig(self):
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
            le_obj_list.extend(self._get_common_basic_line_edits())
            le_obj_list.extend(self._get_all_parameter_line_edits())
            le_obj_list.extend(self.getSameWidget(self.ui.draw_groupbox, QLineEdit))
            le_obj_list = self._unique_widgets_by_object_name(le_obj_list)
            for obj in le_obj_list:
                if config.has_option(section_name, obj.objectName()):
                    obj.setText(config.get(section_name, obj.objectName()))
            for obj in self._get_parameter_checkboxes():
                if config.has_option(section_name, obj.objectName()):
                    obj.setChecked(config.getboolean(section_name, obj.objectName()))
            # obj_list_manual = [self.ui.savedir_lineEdit]
            # for obj in obj_list_manual:
            #     obj.setText(config.get(section_name, obj.objectName()))
            logMsg = "History parameters have been loaded"
            self.addLogMsgWithBar(logMsg)
        except Exception as e:
            errMsg = f"GTE OLD PARA ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)

    def saveConfigPara(self, dir_path=None):
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
            le_obj_list.extend(self._get_current_parameter_line_edits())
            le_obj_list.extend(self._get_all_parameter_line_edits())
            le_obj_list.extend(self._get_common_basic_line_edits())
            le_obj_list.extend(self.getSameWidget(self.ui.draw_groupbox, QLineEdit))
            le_obj_list = self._unique_widgets_by_object_name(le_obj_list)
            for obj in le_obj_list:
                config.set(section_name, obj.objectName(), obj.text())
            for obj in self._get_parameter_checkboxes():
                config.set(section_name, obj.objectName(), str(obj.isChecked()))
            # ========这一部分需要手动添加=====
            # obj_list_manual = [self.ui.savedir_lineEdit]
            # for obj in obj_list_manual:
            #     config.set(section_name, obj.objectName(), obj.text())
            target_dir = dir_path or BASEDIR
            configPath = os.path.join(target_dir, "config.ini")
            with open(configPath, mode="w", encoding="utf-8") as f:
                config.write(f)
            self.logger.debug("Parameters have been saved")
        except Exception as e:
            errMsg = f"PARA SAVE ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)

    def getSameWidget(self, widgetName, activeXName):
        """
        获取某个 widget 中同类型的控件
        :param widgetName: widget名，传入的是ui中的某个widget名
        :param activeXName: 控件类型，传入的是对象
        :return: 寻找到的对象集合(List)
        """
        return widgetName.findChildren(activeXName)
    
    def stopThread(self, thread):
        """
        多进程中进程的停止
        :param thread: 需传入对应的进程
        :return: 无返回值
        """
        try:
            thread.quit()
            thread.wait()
            self.logger.debug(f"Exit {thread.currentThread()} thread，Now state:{thread.isRunning()}")
        except Exception as e:
            errMsg = f"PRECESS EXIT ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)

    
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

    def switchMode(self):
        mode = self.ui.comboBox.currentText()
        self.update_parameter_page_for_mode(mode)
        if mode == "vibration" or mode == "vibration_irregular" or mode == "vibration_square" or mode == "vibration_sine"or mode=="vibration_triangle":
            self.ui.stackedWidget.setCurrentWidget(self.vibration_widget)
            self.ui.stackedWidget_button.setCurrentWidget(self.vibbuttonwidget)
        elif mode == "piezo_calibration":
            self.ui.stackedWidget.setCurrentWidget(self.pcalibration_widget)
            self.ui.stackedWidget_button.setCurrentWidget(self.pcabuttonwidget)

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
                # 加载文件成功之后，应当对运行按钮进行释放
                if self.ui.comboBox.currentText() != "piezo_calibration":
                    self.vibbutton_ui.run_pushButton.setEnabled(True)
                    self.add_textBrowser_str(f"{len(file_list)} vibration files have been loaded:")
                else:
                    self.pcabutton_ui.run_pushButton.setEnabled(True)
                    self.add_textBrowser_str(f"{len(file_list)} piezo_calibration files have been loaded:")
                self.add_textBrowser_list(file_list)
                self.add_textBrowser_str("*" * 45, showtime=False)
                self.add_statusBar_str("File loading completed.")
                self.logger.debug("File loading completed.")
        except Exception as e:
            errMsg = f"DATA FILE LOAD ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)

    def checkDataset(self, dataset):
        """
        检查每个进程计算的数据
        :param dataset:
        :return:
        """
        if not dataset:
            return False
        else:
            if self.keyPara['mode'] == "vibration":
                data_s_e, data_square_wave_s_e = dataset[2], dataset[3]
                data_s_e = np.array(data_s_e)
                data_square_wave_s_e = np.array(data_square_wave_s_e)
                if data_s_e.shape[0] == 0 or data_square_wave_s_e.shape[0] == 0:
                    return False
                return True
            else:
                len_s_e = dataset[2]
                if len_s_e.shape[0] == 0:
                    return False
                return True

    def getAggregateData(self, datasets):
        """
        获取多进程计算结果的聚合
        :param datasets: 多线程的结果
        :return:
        """
        # vibration模块
        if self.keyPara['mode'] == 'vibration':
            print("11111")
            if len(datasets) == 1:
                if self.checkDataset(datasets[0]):
                    return (datasets[0][0], datasets[0][1], datasets[0][2], # log,piezo,data_s_e
                        datasets[0][3], datasets[0][4], datasets[0][5],datasets[0][6],True) # data_wave_s_e,start_point,end_point
                else: 
                    errMsg = "vibration:No valid drawing data, please adjust data"
                    self.addErrorMsgWithBox(errMsg)
                    return None, None, None, None, None,None,None,False
            else:
                effectCount = 0
                df_logG, df_piezo,data_s_e,data_square_wave_s_e, start_point, end_point,valid_num = None,None,None,None,None,None,None
                for dataset in datasets:
                    if self.checkDataset(dataset):
                        if effectCount == 0:
                            df_logG, df_piezo,data_s_e= dataset[0], dataset[1], dataset[2]
                            data_square_wave_s_e, start_point, end_point = dataset[3], dataset[4], dataset[5]
                            valid_num = dataset[6]
                        else:
                            data_s_e = np.concatenate((data_s_e, dataset[2]+len(df_logG)))
                            data_square_wave_s_e = np.concatenate((data_square_wave_s_e, dataset[3]+len(df_logG)))
                            start_point = np.concatenate((start_point, dataset[4]+len(df_logG)))
                            end_point = np.concatenate((end_point, dataset[5]+len(df_logG)))
                            df_logG = np.concatenate((df_logG, dataset[0]))
                            df_piezo = np.concatenate((df_piezo, dataset[1]))
                            valid_num += dataset[6]
                        effectCount += 1
                        print("22222")
                if effectCount == 0:
                    errMsg = "vibration:No valid drawing data, please adjust data"
                    self.addErrorMsgWithBox(errMsg)
                    return None, None, None, None, None,None,None,False
                else:
                    return df_logG, df_piezo,data_s_e,data_square_wave_s_e, start_point, end_point,valid_num,True
        #calibration模块
        else:
            if len(datasets) == 1:
                if self.checkDataset(datasets[0]):
                    return (datasets[0][0], datasets[0][1], datasets[0][2], # delta_piezo_voltage,data_s_e,len_s_e,valid_num
                        datasets[0][3],True)
                else: 
                    errMsg = "piezocalibration:No valid drawing data, please adjust data"
                    self.addErrorMsgWithBox(errMsg)
                    return None, None, None ,None, False
            else:
                effectCount = 0
                delta_piezo_voltage,data_s_e,len_s_e,valid_num = None,None,None,None
                for dataset in datasets:
                    if self.checkDataset(dataset):
                        if effectCount == 0:
                            delta_piezo_voltage, data_s_e,len_s_e= dataset[0], dataset[1], dataset[2]
                            valid_num = dataset[3]
                        else:
                            len_s_e = np.concatenate((len_s_e, dataset[2]))
                            delta_piezo_voltage = np.concatenate((delta_piezo_voltage, dataset[0]))
                            data_s_e = np.concatenate((data_s_e, dataset[1]))
                            valid_num += dataset[3]
                        effectCount += 1
                if effectCount == 0:
                    errMsg = "piezocalibration::No valid drawing data, please adjust data"
                    self.addErrorMsgWithBox(errMsg)
                    return None, None, None, None,False
                else:
                    return delta_piezo_voltage, data_s_e,len_s_e,valid_num,True
            

    def VibRunProcess(self):
        try:
            self.ui.progressBar.setValue(0)
            # 每次开始新运行时重置退出标志
            self.is_quit = False
            self.vibbutton_ui.run_pushButton.setEnabled(False)  # 这里需要注意的是点击一次run 控件之后，应当设置未为不可选，
            self.vibbutton_ui.save_pushButton.setEnabled(False)
            self.ui.redraw_pushButton.setEnabled(False)
            self.keyPara["viSaveData_Statue"] = False

            keyPara = self.getPanelPara()
            keyPara['mode'] = self.ui.comboBox.currentText()
            keyPara['single_draw'] = True
            keyPara['run_data'] = True
            if self.cut_para_ui.range_open_checkBox.isChecked():
                keyPara['conda_range_check'] = True
            else:
                keyPara['conda_range_check'] = False
            if keyPara is None:
                return
            else:
                self.keyPara.update(keyPara)
                self.logger.debug(f"vibration:Parameters are updated before running. Parameter list:{self.keyPara}")
                self.dataThread = QThread()
                self.dataAnalysis = DataAnalysismodel(self.keyPara)
                self.dataAnalysis.runEnd.connect(lambda: self.stopThread(self.dataThread))

                self.dataAnalysis.moveToThread(self.dataThread)
                # Use a wrapper so we can prevent Run() execution if user requested quit
                self.dataThread.started.connect(self._on_dataThread_started)
                self.dataThread.finished.connect(self.VibdrawPre)

                logMsg = "vibration:Data calculation..."
                self.addLogMsgWithBar(logMsg)
                self.dataThread.start()
                self.logger.debug(
                    f"vibration:Start the data calculation thread--{self.dataThread.currentThread()},Now state:{self.dataThread.isRunning()}")
                self.set_progress_value(10)
        except Exception as e:
            errMsg = f"vibration:RUN ERROR:{e}"
            self.set_progress_value(0)
            self.addErrorMsgWithBox(errMsg)
    


    def VibdrawPre(self):
        self.ui.progressBar.setValue(80)
        if getattr(self, 'is_quit', False):
            self.addLogMsgWithBar("vibration:Drawing skipped because process was terminated.")
            return
        self.logger.debug("vibration:The computing process exits safely and begins computing drawing data")
        self.datasets = self.dataAnalysis.datasets
        # 这里的这个返回值是多进程的返回数据的集合！
        # 不管是单个文件，还是多个文件，都是List

        try:
            if  self.keyPara['mode'] != 'vibration':
                self.cond_axis_corr_x,self.cond_axis_corr_y,self.log_G_peak,self.log_G_trough,self.valid_num_vi,statue = getDrawData(self.datasets,self.keyPara)
            else:
                self.df_logG_vi, self.df_piezo_vi,self.data_s_e_vi,self.data_square_wave_s_e_vi, self.start_point_vi, self.end_point_vi,self.valid_num_vi,statue = self.getAggregateData(self.datasets)
            
        except Exception as e:
            errMsg = f"vibration:The parallel computing draw data aggregation error:{e}"
            self.ui.progressBar.setValue(0)
            self.addErrorMsgWithBox(errMsg)
            self.vibbutton_ui.run_pushButton.setEnabled(True)
        else:
            if not statue:
                errMsg = f"No Valid Data!"
                self.ui.progressBar.setValue(60)
                self.addErrorMsgWithBox(errMsg)
                return
            else:
                self.addLogMsgWithBar(f"vibration:All trace: {self.valid_num_vi}.")
                logMsg = f"vibration:Start drawing..."
                self.addLogMsgWithBar(logMsg)
                try:
                    self.Vibdraw(self.valid_num_vi)
                except Exception as e:
                    errMsg = f"vibration:DRAW ERROR:{e}"
                    self.ui.progressBar.setValue(0)
                    self.addErrorMsgWithBox(errMsg)
                else:
                    self.ui.redraw_pushButton.setEnabled(True)
                    # 如果绘制成功且数据可用，允许打开单条筛选窗口
                    try:
                        self.ui.singleFilter_pushButton.setEnabled(True)
                    except Exception:
                        self.ui.progressBar.setValue(0)
        finally:
            self.vibbutton_ui.run_pushButton.setEnabled(True)

    def data_axis_corr(self,log_G, data_s_e, wave_start_point, sampling_frequency=20000):
        data_s_e1 = np.array(data_s_e)
        cond_axis_corr_x = []
        cond_axis_corr_y = []
        for i in range(len(data_s_e)):
            ii = wave_start_point[i] - data_s_e1[i, 0]
            for j in range(0, data_s_e1[i, 1] - data_s_e1[i, 0]):
                cond_axis_corr_x.append((j - ii) / sampling_frequency)
                cond_axis_corr_y.append(log_G[j + data_s_e1[i, 0]])
        return cond_axis_corr_x, cond_axis_corr_y

    def one_D_conductance_histogram_square_wave(self,log_G, piezo_voltage, start_point, end_point, piezo_amplitude):
        log_G_peak = []
        log_G_trough = []
        pv = np.asarray(piezo_voltage)
        for i in range(len(start_point)):
            segment = pv[start_point[i]:end_point[i]]
            diff_segment = np.diff(segment)
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(diff_segment, prominence=(piezo_amplitude * 1.8))
            trough_peaks, _ = find_peaks(-diff_segment, prominence=(piezo_amplitude * 1.8))
            switch_point = np.sort(np.concatenate((peaks, trough_peaks)))
            if len(peaks) > 0 and len(trough_peaks) > 0 and min(switch_point) == min(peaks):
                for j in range(0, len(switch_point) - 1, 2):
                    start_idx = start_point[i] + switch_point[j] + 50
                    end_idx = start_point[i] + switch_point[j + 1] - 50
                    log_G_peak.extend(log_G[start_idx:end_idx])
                for j in range(1, len(switch_point) - 1, 2):
                    start_idx = start_point[i] + switch_point[j] + 50
                    end_idx = start_point[i] + switch_point[j + 1] - 50
                    log_G_trough.extend(log_G[start_idx:end_idx])
            elif len(peaks) > 0 and len(trough_peaks) > 0 and min(switch_point) == min(trough_peaks):
                for j in range(0, len(switch_point) - 1, 2):
                    start_idx = start_point[i] + switch_point[j] + 50
                    end_idx = start_point[i] + switch_point[j + 1] - 50
                    log_G_trough.extend(log_G[start_idx:end_idx])
                for j in range(1, len(switch_point) - 1, 2):
                    start_idx = start_point[i] + switch_point[j] + 50
                    end_idx = start_point[i] + switch_point[j + 1] - 50
                    log_G_peak.extend(log_G[start_idx:end_idx])
        return log_G_peak, log_G_trough
    
    def _on_dataThread_started(self):
            # This runs in the main thread when the QThread starts. We decide whether
            # to actually call DataAnalysismodel.Run. Use QMetaObject.invokeMethod with
            # QueuedConnection to ensure Run() executes in the dataAnalysis object's thread.
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
    
    def Vibdraw(self,valid_num:int):
        sampfrequency = self.keyPara['sample_frequence_lineEdit']
        binsx = int(self.keyPara['binsx_lineEdit'])  
        binsy = int(self.keyPara['binsy_lineEdit']) 
        cmin = int(self.keyPara['cmin_lineEdit']) 
        vmax = int(self.keyPara['colormax_lineEdit']) if (int(self.keyPara['colormax_lineEdit'])) != 0 else None
        xmax = float(self.keyPara['x_2d_max_lineEdit']) if (float(self.keyPara['x_2d_max_lineEdit'])) != -10 else None
        xmin = float(self.keyPara['x_2d_min_lineEdit']) if (float(self.keyPara['x_2d_min_lineEdit'])) != -10 else None
        ymax = float(self.keyPara['G_max_lineEdit'])
        ymin = float(self.keyPara['G_min_lineEdit'])
        if  self.keyPara['mode'] != 'vibration':
            cond_axis_x,cond_axis_y = self.cond_axis_corr_x,self.cond_axis_corr_y
            log_G_peak,log_G_trough = self.log_G_peak,self.log_G_trough
        else:
            cond_axis_x,cond_axis_y = self.data_axis_corr(self.df_logG_vi,self.data_square_wave_s_e_vi, self.start_point_vi,sampling_frequency=sampfrequency)
            log_G_peak,log_G_trough = self.one_D_conductance_histogram_square_wave(self.df_logG_vi,self.df_piezo_vi,self.start_point_vi, self.end_point_vi,piezo_amplitude=piezoamp)
        if xmax is None :
            xmax = max(cond_axis_x)
        if xmin is None :
            xmin = min(cond_axis_x)
        # print(log_G_peak)
        dbins1 = int(self.keyPara['d1bins_lineEdit'])
        # counts, bins = np.histogram(log_G_peak, bins=dbins1)
        # counts = counts / np.sum(counts)  # 概率化（每个 bin 占总样本比例）
        # 清空并创建两个子图
        self.vib_2dcanvas.figure.clf()
        # gs = self.vib_2d1dcanvas.figure.add_gridspec(1, 2, width_ratios=[3, 1])
        # ax1 = self.vib_2d1dcanvas.figure.add_subplot(gs[0,0])
        ax1 = self.vib_2dcanvas.figure.add_subplot()
        # ax2 = self.vib_2d1dcanvas.figure.add_subplot(gs[0, 1], sharey=ax1)
        # 2D直方图
        h = ax1.hist2d(cond_axis_x, cond_axis_y, cmin=cmin, vmax=vmax,
                    bins=[binsx, binsy],
                    range=[[xmin, xmax], [ymin, ymax]],
                    cmap=self.keyPara.get('ColorMap', 'rainbow'))
        # 保存二维直方图矩阵（counts）和边界
        try:
            H = h[0]
            xedges = h[1]
            yedges = h[2]
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
        ax1.set_ylim(self.keyPara.get('G_min_lineEdit', -6), self.keyPara.get('G_max_lineEdit', 0))
        self.vib_2dcanvas.figure.colorbar(h[3], ax=ax1)
        # ax1.set_xlim(-0.2, 0.6)
        self.vib_1dcanvas.figure.clf()
        if self.keyPara['mode'] != 'vibration_irregular':
            ax2 = self.vib_1dcanvas.figure.add_subplot()
            # 1D概率分布 — 先计算原始计数以便保存，再归一化用于绘图
            raw_peak_counts, peak_bins = np.histogram(log_G_peak, bins=dbins1,range=[ymin, ymax])
            raw_trough_counts, trough_bins = np.histogram(log_G_trough, bins=dbins1,range=[ymin, ymax])
            # 保存原始计数（整数）和 bin 边界
            try:
                self.peakH = raw_peak_counts.astype(int)
                self.troughH = raw_trough_counts.astype(int)
                self.peak_bins = peak_bins
                self.trough_bins = trough_bins
            except Exception:
                self.peakH = None
                self.troughH = None
                self.peak_bins = None
                self.trough_bins = None

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
            ax2.set_ylim(self.keyPara.get('G_min_lineEdit', -6), self.keyPara.get('G_max_lineEdit', 0))
            ax2.legend(['Peak','Trough'])
            ax2.grid(True)
        self.vib_2dcanvas.draw()
        self.vib_1dcanvas.draw()
        self.vib_2dcanvas.flush_events()
        self.vib_1dcanvas.flush_events()
        
        
        # 绘图结束
        logMsg = "vibration:Draw finished"
        self.addLogMsgWithBar(logMsg)
        self.keyPara["viSaveData_Statue"] = True  # 这个true放在这里的目的是只要绘图完成一遍，就说明产生了新数据，可以保存
        self.vibbutton_ui.save_pushButton.setEnabled(True)
        self.vibbutton_ui.run_pushButton.setEnabled(True)
        if self.keyPara['run_data'] and self.keyPara['mode'] != 'vibration':
            if hasattr(self, 'single_trace_window') and self.single_trace_window is not None:
                self.single_trace_window.load_data(datasets=getattr(self, 'datasets', []), lastOpenPath=getattr(self, 'lastOpenPath', ''), source='main')
                self.keyPara['run_data'] = False
        # 如果 single_trace_window 已存在且允许主程序覆盖（None 或 'main'），则更新其 datasets
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
            self.ui.progressBar.setValue(0)
        self.ui.progressBar.setValue(100)
    
    def open_single_trace_window(self):
        keyPara = self.getPanelPara()
        keyPara['mode'] = self.ui.comboBox.currentText()
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
        keyPara['mode'] = self.ui.comboBox.currentText()
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
                    cond_x, cond_y, log_G_peak, log_G_trough, valid_num, ok = getDrawData(chosen_indices, self.keyPara)
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
                self.Vibdraw(valid_num)
                return
        except Exception as e:
            self.addErrorMsgWithBox(f"Redraw from single trace failed: {e}")
    
    # piezo_calibration模块的运行
    def PcaRunProcess(self):
        try:
            # 每次开始新运行时重置退出标志
            self.is_quit = False
            self.pcabutton_ui.run_pushButton.setEnabled(False)  # 这里需要注意的是点击一次run 控件之后，应当设置未为不可选，
            self.pcabutton_ui.save_pushButton.setEnabled(False)
            self.ui.redraw_pushButton.setEnabled(False)
            self.keyPara["pcaSaveData_Statue"] = False

            keyPara = self.getPanelPara()
            keyPara['mode'] = self.ui.comboBox.currentText()
            if keyPara is None:
                return
            else:
                self.keyPara.update(keyPara)
                self.logger.debug(f"piezocalibration:Parameters are updated before running. Parameter list:{self.keyPara}")
                self.dataThread = QThread()
                self.dataAnalysis = DataAnalysismodel(self.keyPara)
                self.dataAnalysis.runEnd.connect(lambda: self.stopThread(self.dataThread))

                self.dataAnalysis.moveToThread(self.dataThread)
                # Use a wrapper so we can prevent Run() execution if user requested quit
                self.dataThread.started.connect(self._on_dataThread_started)
                self.dataThread.finished.connect(self.PcadrawPre)

                logMsg = "piezocalibration:Data calculation..."
                self.addLogMsgWithBar(logMsg)

                self.dataThread.start()
                self.logger.debug(
                    f"piezocalibration:Start the data calculation thread--{self.dataThread.currentThread()},Now state:{self.dataThread.isRunning()}")
        except Exception as e:
            errMsg = f"piezocalibration:RUN ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
    
    def PcadrawPre(self):   
        # 如果在绘图之前用户已请求退出，则直接返回
        if getattr(self, 'is_quit', False):
            self.addLogMsgWithBar("piezocalibration:Drawing skipped because process was terminated.")
            return
        self.logger.debug("piezocalibration:The computing process exits safely and begins computing drawing data")
        datasets = self.dataAnalysis.datasets
        # 这里的这个返回值是多进程的返回数据的集合！
        # 不管是单个文件，还是多个文件，都是List

        try:
            self.delta_piezo_voltage, self.data_s_e_vi,self.len_s_e,self.valid_num_vi,statue = self.getAggregateData(datasets)
        except Exception as e:
            errMsg = f"piezocalibration:The parallel computing draw data aggregation error:{e}"
            self.addErrorMsgWithBox(errMsg)
            self.pcabutton_ui.run_pushButton.setEnabled(True)
        else:
            if not statue:
                return
            else:
                self.addLogMsgWithBar(f"piezocalibration:All trace: {self.valid_num_vi}.")
                logMsg = f"piezocalibration:Start drawing..."
                self.addLogMsgWithBar(logMsg)

                try:
                    self.Pcadraw()
                except Exception as e:
                    errMsg = f"piezocalibration:DRAW ERROR:{e}"
                    self.addErrorMsgWithBox(errMsg)
                else:
                    self.ui.redraw_pushButton.setEnabled(True)
        finally:
            self.pcabutton_ui.run_pushButton.setEnabled(True)
    @staticmethod
    def gauss(x, a1, b1, c1):
        return a1 * np.exp(-((x - b1) / c1) ** 2)
    def Pcadraw(self):
        if getattr(self, 'is_quit', False):
            self.addLogMsgWithBar("vibration:Drawing skipped because process was terminated.")
            return
        x_l = float(self.keyPara['xl_lineEdit'])
        x_h = float(self.keyPara['xh_lineEdit'])
        bins_num = int(self.keyPara['pbins_lineEdit'])
        ax = self.piezo_1dcanvas.figure.axes[0] if self.piezo_1dcanvas.figure.axes else self.piezo_1dcanvas.figure.add_subplot(111)
        ax.clear()  # 清空当前Axes，而不是整个figure
        counts, bins, patches = ax.hist(self.delta_piezo_voltage,bins=bins_num)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        # self.addLogMsgWithBar(f"{bin_centers}")
        self.pcabinsvalue = np.column_stack((bin_centers,counts))
        # a0 = np.max(counts)
        # b0 = bin_centers[np.argmax(counts)]
        # c0 = (x_h - x_l) / 10
        # p0 = [a0, b0, c0]
        # ===== 6. 拟合高斯曲线 =====
        from scipy.optimize import curve_fit
        try:
            popt, _ = curve_fit(self.gauss, bin_centers, counts, maxfev=10000)
            a1, b1, c1 = popt
            # 输出峰值
            self.addLogMsgWithBar(f"piezocalibration: 峰值为 {b1:.6f}")
        except Exception as e:
            self.addLogMsgWithBar(f"piezocalibration: 高斯拟合失败 ({e})")
            a1 = b1 = c1 = np.nan
        # 用非线性最小二乘法拟合
        # popt,_ = curve_fit(self.gauss1,x,ydata,maxfev=10000)
        # a1,b1,c1 = popt
        # self.addLogMsgWithBar(f"piezocalibration:峰值为: {b1:.3f}.")
        # # 计算拟合曲线
        # y = np.array([a1 * np.exp(-((xi - b1) / c1) ** 2) for xi in x])
        x_fit = np.linspace(x_l, x_h, 500)
        y_fit = self.gauss(x_fit, a1, b1, c1)
        self.gussvalue = np.column_stack((x_fit,y_fit))
        ax.plot(x_fit, y_fit, 'r-', linewidth=2, label='Gaussian Fit')
        # ax.plot(x,y,'r-')
        ax.set_xlim(x_l,x_h)
        ax.set_xlabel("delta piezo voltage")
        ax.set_ylabel("Counts")
        self.piezo_1dcanvas.draw()
        self.piezo_1dcanvas.flush_events()
        # 绘图结束
        logMsg = "piezocalibration:Draw finished"
        self.addLogMsgWithBar(logMsg)
        self.keyPara["pcaSaveData_Statue"] = True  # 这个true放在这里的目的是只要绘图完成一遍，就说明产生了新数据，可以保存
        self.pcabutton_ui.save_pushButton.setEnabled(True)
        self.pcabutton_ui.run_pushButton.setEnabled(True)
        
    # 重画按钮
    def BtnRedrawClicked(self):
        try:
            keyPara = self.getPanelPara()
            if keyPara is None:
                return
            else:
                self.keyPara.update(keyPara)
                self.logger.debug(f"Parameters are updated before running. Parameter list:{self.keyPara}")
                if self.ui.comboBox.currentText() != "piezo_calibration":
                    self.vibbutton_ui.save_pushButton.setEnabled(False)
                    self.vibbutton_ui.run_pushButton.setEnabled(False)
                    self.Vibdraw(self.valid_num_vi)
                else:
                    self.pcabutton_ui.save_pushButton.setEnabled(False)
                    self.pcabutton_ui.run_pushButton.setEnabled(False)
                    self.Pcadraw()
        except Exception as e:
            errMsg = f"REDRAW ERROR:{e}"
            self.addErrorMsgWithBox(errMsg)
            self.vibbutton_ui.run_pushButton.setEnabled(True)
            
    #保存数据

            
    def VibActSaveData(self):
            try:
                preCheck = self.savePreCheck()
                if preCheck:
                    # finished check
                    dataSavePath = self.keyPara["Data_Save_Path"]

                    # fig save
                    self.VibsaveFig(dataSavePath)
                    # end fig save

                    # data save
                    self.VibsaveData(dataSavePath)
                    # end data save

                    logMsg = f"All data has been saved. Path:{dataSavePath}"
                    self.addLogMsgWithBar(logMsg)
                    QMessageBox.information(self, "Info", logMsg)
            except Exception as e:
                errMsg = f"DATA SAVE ERROR:{e}"
                self.addErrorMsgWithBox(errMsg)
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
            self.vib_2dcanvas.figure.savefig(d2Path, dpi=100, bbox_inches='tight')
            if self.keyPara['mode'] != 'vibration_irregular':
                self.vib_1dcanvas.figure.savefig(d1Path, dpi=100, bbox_inches='tight')
    def zero_pad(self, x_2D_edges, y_2D_edges):
        x_use = x_2D_edges[1:]
        y_use = y_2D_edges[1:]
        len_x = len(x_use)
        len_y = len(y_use)

        if len_x < len_y:
            _PAD_NUM = len_y - len_x
            x_2D_edges_pad = np.pad(x_use, (0, _PAD_NUM), 'constant', constant_values=(0))
            y_2D_edges_pad = y_use
        else:
            _PAD_NUM = len_x - len_y
            x_2D_edges_pad = x_use
            y_2D_edges_pad = np.pad(y_use, (0, _PAD_NUM), 'constant', constant_values=(0))
        return x_2D_edges_pad, y_2D_edges_pad
    def VibsaveData(self, dataSavePath):
        """
        数据保存
        :param dataSavePath:
        :return:
        """
        dataPath = os.path.join(dataSavePath, "imgData")
        GeneralUtils.creatFolder(dataSavePath, "imgData")
        d2Path = os.path.join(dataPath, "2Dcond.txt")
        peakPath = os.path.join(dataPath, "Log_G_Peak.txt")
        troughPath = os.path.join(dataPath, "Log_G_trough.txt")
        if hasattr(self, 'd2H') and self.d2H is not None:
            H = np.nan_to_num(self.d2H, nan=0.0)  # 替换 NaN 为 0
            np.savetxt(d2Path, H, fmt='%.6f', delimiter='\t')
            x_2dbins, y_2dbins = self.zero_pad(self.d2_xedges,self.d2_yedges)
            np.savetxt(os.path.join(dataPath, "2Dcond_xedges.txt"), x_2dbins, fmt='%.6f', delimiter='\t')
            np.savetxt(os.path.join(dataPath, "2Dcond_yedges.txt"), y_2dbins, fmt='%.6f', delimiter='\t')
        if self.keyPara['mode'] != 'vibration_irregular':
            if hasattr(self, 'peak_bins') and self.peak_bins is not None:
                peak_centers = (self.peak_bins[:-1] + self.peak_bins[1:]) / 2
                peak_data = np.column_stack((peak_centers, self.peakH))
                np.savetxt(peakPath, peak_data, fmt='%.6f', delimiter='\t')
                np.savetxt(os.path.join(dataPath, "Log_G_Peak_bins.txt"), self.peak_bins, fmt='%.6f', delimiter='\t')
            if hasattr(self, 'trough_bins') and self.trough_bins is not None:
                peak_centers = (self.trough_bins[:-1] + self.trough_bins[1:]) / 2
                peak_data = np.column_stack((peak_centers, self.troughH))
                np.savetxt(troughPath, peak_data, fmt='%.6f', delimiter='\t')
                np.savetxt(os.path.join(dataPath, "Log_G_trough_bins.txt"), self.trough_bins, fmt='%.6f', delimiter='\t')

    # 保存矫正数据
    def PcaActSaveData(self):
            try:
                preCheck = self.savePreCheck()
                if preCheck:
                    # finished check
                    dataSavePath = self.keyPara["Data_Save_Path"]

                    # fig save
                    self.PcasaveFig(dataSavePath)
                    # end fig save

                    # data save
                    self.PcasaveData(dataSavePath)
                    # end data save

                    logMsg = f"piezocalibration:All data has been saved. Path:{dataSavePath}"
                    self.addLogMsgWithBar(logMsg)
                    QMessageBox.information(self, "Info", logMsg)
            except Exception as e:
                errMsg = f"piezocalibration:DATA SAVE ERROR:{e}"
                self.addErrorMsgWithBox(errMsg)
    def PcasaveFig(self, dataSavePath):
            """
            图片保存
            :param dataSavePath:
            :return:
            """
            imgPath = os.path.join(dataSavePath, "Images")
            GeneralUtils.creatFolder(dataSavePath, "Images")
            dPath = os.path.join(imgPath, "2D-1D.png")
            self.piezo_1dcanvas.figure.savefig(dPath, dpi=100, bbox_inches='tight')

    def PcasaveData(self, dataSavePath):
        """
        数据保存
        :param dataSavePath:
        :return:
        """
        dataPath = os.path.join(dataSavePath, "Data")
        GeneralUtils.creatFolder(dataSavePath, "Data")
        d1Path = os.path.join(dataPath, "1Dhist.txt")

        np.savetxt(d1Path, self.pcabinsvalue, fmt='%.6f', delimiter='\t')
        np.savetxt(os.path.join(dataPath, "1Dhist_guassfit.txt"), self.gussvalue, fmt='%.6f', delimiter='\t')
    def savePreCheck(self):
        """
        数据保存之前的检查
        :return:
        """
        if not self.keyPara["viSaveData_Statue"] and self.ui.comboBox.currentText() != "piezo_calibration":
            errMsg = f"{self.ui.comboBox.currentText()}:The data cannot be saved until the data processing is complete!"
            self.addErrorMsgWithBox(errMsg)
            return False
        if not self.keyPara["pcaSaveData_Statue"] and self.ui.comboBox.currentText() == "piezo_calibration":
            errMsg = "piezocalibration:The data cannot be saved until the data processing is complete!"
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
            if self.ui.comboBox.currentText() != "piezo_calibration":
                defaultName = f"VibrationAnalysis{formatted_time}"
            else:
                defaultName = f"PiezoCalibration{formatted_time}"
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
            # 退出前询问是否删除文件对应的缓存文件
            file_list = self.keyPara.get('FILE_PATHS') if isinstance(self.keyPara, dict) else None
            cache_paths = []
            if file_list and isinstance(file_list, (list, tuple)):
                for file_path in file_list:
                    if isinstance(file_path, str):
                        cache_file = file_path + ".cache.npz"
                        if os.path.exists(cache_file):
                            cache_paths.append(cache_file)
            if cache_paths:
                cache_question = (
                    "Do you want to delete all corresponding '.cache.npz' files before exit?\n"
                    "if you still need to analyze these files later on ,please do not delete them.This will speed up the analysis of TDMS files\n"
                    "if not,please delete them to save disk space\n"
                )
                cache_reply = QMessageBox.question(self, "Delete Cache Files", cache_question,
                                                   QMessageBox.Yes | QMessageBox.No,
                                                   QMessageBox.No)
                if cache_reply == QMessageBox.Yes:
                    for cache_file in cache_paths:
                        try:
                            os.remove(cache_file)
                        except Exception as e:
                            self.logger.error(f"Failed to delete cache file {cache_file}: {e}")
            self.saveConfigPara()
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
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = VibrationAnalysis()
    window.show()
    sys.exit(app.exec())
