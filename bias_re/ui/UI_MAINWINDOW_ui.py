# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_MAINWINDOW.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)
import ui.images_rc

class Ui_BasicanalysisWindow(object):
    def setupUi(self, BasicanalysisWindow):
        if not BasicanalysisWindow.objectName():
            BasicanalysisWindow.setObjectName(u"BasicanalysisWindow")
        BasicanalysisWindow.resize(1290, 821)
        BasicanalysisWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(BasicanalysisWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_12 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.open_pushButton = QToolButton(self.centralwidget)
        self.open_pushButton.setObjectName(u"open_pushButton")
        self.open_pushButton.setMinimumSize(QSize(60, 40))
        self.open_pushButton.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.open_pushButton.setFont(font)
        icon = QIcon()
        icon.addFile(u":/png/images/openfile.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_pushButton.setIcon(icon)
        self.open_pushButton.setIconSize(QSize(20, 20))
        self.open_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.open_pushButton)

        self.run_pushButton = QToolButton(self.centralwidget)
        self.run_pushButton.setObjectName(u"run_pushButton")
        self.run_pushButton.setMinimumSize(QSize(60, 40))
        self.run_pushButton.setMaximumSize(QSize(60, 16777215))
        self.run_pushButton.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/png/images/run.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run_pushButton.setIcon(icon1)
        self.run_pushButton.setIconSize(QSize(20, 20))
        self.run_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.run_pushButton)

        self.view_pushButton = QToolButton(self.centralwidget)
        self.view_pushButton.setObjectName(u"view_pushButton")
        self.view_pushButton.setMinimumSize(QSize(60, 40))
        self.view_pushButton.setMaximumSize(QSize(60, 16777215))
        self.view_pushButton.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u":/png/images/view.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.view_pushButton.setIcon(icon2)
        self.view_pushButton.setIconSize(QSize(25, 25))
        self.view_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.view_pushButton)

        self.save_pushButton = QToolButton(self.centralwidget)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setMinimumSize(QSize(60, 40))
        self.save_pushButton.setMaximumSize(QSize(60, 16777215))
        self.save_pushButton.setFont(font)
        icon3 = QIcon()
        icon3.addFile(u":/png/images/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_pushButton.setIcon(icon3)
        self.save_pushButton.setIconSize(QSize(20, 20))
        self.save_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.save_pushButton)

        self.quit_pushButton = QToolButton(self.centralwidget)
        self.quit_pushButton.setObjectName(u"quit_pushButton")
        self.quit_pushButton.setMinimumSize(QSize(60, 40))
        self.quit_pushButton.setMaximumSize(QSize(80, 16777215))
        self.quit_pushButton.setFont(font)
        icon4 = QIcon()
        icon4.addFile(u":/png/images/quit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.quit_pushButton.setIcon(icon4)
        self.quit_pushButton.setIconSize(QSize(20, 20))
        self.quit_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.quit_pushButton)

        self.about_pushButton = QToolButton(self.centralwidget)
        self.about_pushButton.setObjectName(u"about_pushButton")
        self.about_pushButton.setMinimumSize(QSize(60, 40))
        self.about_pushButton.setMaximumSize(QSize(80, 16777215))
        self.about_pushButton.setFont(font)
        icon5 = QIcon()
        icon5.addFile(u":/png/images/about.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.about_pushButton.setIcon(icon5)
        self.about_pushButton.setIconSize(QSize(20, 20))
        self.about_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.about_pushButton)

        self.wave_select_comboBox = QComboBox(self.centralwidget)
        self.wave_select_comboBox.setObjectName(u"wave_select_comboBox")
        self.wave_select_comboBox.setMinimumSize(QSize(100, 40))
        self.wave_select_comboBox.setMaximumSize(QSize(200, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.wave_select_comboBox.setFont(font1)

        self.horizontalLayout_8.addWidget(self.wave_select_comboBox)

        self.singleselect_pushButton = QToolButton(self.centralwidget)
        self.singleselect_pushButton.setObjectName(u"singleselect_pushButton")
        self.singleselect_pushButton.setMinimumSize(QSize(60, 40))
        self.singleselect_pushButton.setMaximumSize(QSize(60, 16777215))
        self.singleselect_pushButton.setFont(font)
        icon6 = QIcon()
        icon6.addFile(u":/png/images/select.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.singleselect_pushButton.setIcon(icon6)
        self.singleselect_pushButton.setIconSize(QSize(20, 20))
        self.singleselect_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_8.addWidget(self.singleselect_pushButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(250, 0))
        self.progressBar.setValue(0)

        self.horizontalLayout_8.addWidget(self.progressBar)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.horizontalLayout_8.setStretch(6, 1)
        self.horizontalLayout_8.setStretch(10, 1)

        self.verticalLayout_12.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.draw_stackedWidget = QStackedWidget(self.centralwidget)
        self.draw_stackedWidget.setObjectName(u"draw_stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.draw_stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.draw_stackedWidget.addWidget(self.page_2)

        self.verticalLayout_11.addWidget(self.draw_stackedWidget)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(0, 0))
        self.label_20.setMaximumSize(QSize(16777215, 16777215))
        self.label_20.setFont(font1)

        self.verticalLayout_10.addWidget(self.label_20)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(0, 0))
        self.textBrowser.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.textBrowser.setFont(font2)

        self.verticalLayout_10.addWidget(self.textBrowser)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.verticalLayout_11.setStretch(0, 2)
        self.verticalLayout_11.setStretch(1, 1)

        self.horizontalLayout_7.addLayout(self.verticalLayout_11)

        self.para_tabWidget = QTabWidget(self.centralwidget)
        self.para_tabWidget.setObjectName(u"para_tabWidget")
        self.para_tabWidget.setFont(font1)
        self.Basic_Set_Tab = QWidget()
        self.Basic_Set_Tab.setObjectName(u"Basic_Set_Tab")
        self.verticalLayout_13 = QVBoxLayout(self.Basic_Set_Tab)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.cutPara_groupBox = QGroupBox(self.Basic_Set_Tab)
        self.cutPara_groupBox.setObjectName(u"cutPara_groupBox")
        self.cutPara_groupBox.setMinimumSize(QSize(0, 0))
        self.cutPara_groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.cutPara_groupBox.setFont(font1)
        self.verticalLayout_5 = QVBoxLayout(self.cutPara_groupBox)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 6, 3, 3)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.timelabel_2 = QLabel(self.cutPara_groupBox)
        self.timelabel_2.setObjectName(u"timelabel_2")
        self.timelabel_2.setFont(font2)

        self.gridLayout.addWidget(self.timelabel_2, 1, 3, 1, 1)

        self.time_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.time_lineEdit.setObjectName(u"time_lineEdit")
        self.time_lineEdit.setMinimumSize(QSize(50, 20))
        self.time_lineEdit.setMaximumSize(QSize(100, 40))
        self.time_lineEdit.setFont(font2)

        self.gridLayout.addWidget(self.time_lineEdit, 1, 4, 1, 1)

        self.highcond_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.highcond_lineEdit.setObjectName(u"highcond_lineEdit")
        self.highcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.highcond_lineEdit.setMaximumSize(QSize(100, 40))
        self.highcond_lineEdit.setFont(font2)

        self.gridLayout.addWidget(self.highcond_lineEdit, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.samplefrelabel = QLabel(self.cutPara_groupBox)
        self.samplefrelabel.setObjectName(u"samplefrelabel")
        self.samplefrelabel.setFont(font2)

        self.gridLayout.addWidget(self.samplefrelabel, 2, 0, 1, 1)

        self.lowcond_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.lowcond_lineEdit.setObjectName(u"lowcond_lineEdit")
        self.lowcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.lowcond_lineEdit.setMaximumSize(QSize(100, 40))
        self.lowcond_lineEdit.setFont(font2)

        self.gridLayout.addWidget(self.lowcond_lineEdit, 0, 4, 1, 1)

        self.sample_rate_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.sample_rate_lineEdit.setObjectName(u"sample_rate_lineEdit")
        self.sample_rate_lineEdit.setMinimumSize(QSize(50, 20))
        self.sample_rate_lineEdit.setMaximumSize(QSize(100, 40))
        self.sample_rate_lineEdit.setFont(font2)

        self.gridLayout.addWidget(self.sample_rate_lineEdit, 2, 1, 1, 1)

        self.addlenlabel_2 = QLabel(self.cutPara_groupBox)
        self.addlenlabel_2.setObjectName(u"addlenlabel_2")
        self.addlenlabel_2.setFont(font2)

        self.gridLayout.addWidget(self.addlenlabel_2, 1, 0, 1, 1)

        self.additional_length_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.additional_length_lineEdit.setObjectName(u"additional_length_lineEdit")
        self.additional_length_lineEdit.setMinimumSize(QSize(50, 20))
        self.additional_length_lineEdit.setMaximumSize(QSize(100, 40))
        self.additional_length_lineEdit.setFont(font2)

        self.gridLayout.addWidget(self.additional_length_lineEdit, 1, 1, 1, 1)

        self.highcondlabel_2 = QLabel(self.cutPara_groupBox)
        self.highcondlabel_2.setObjectName(u"highcondlabel_2")
        self.highcondlabel_2.setFont(font2)

        self.gridLayout.addWidget(self.highcondlabel_2, 0, 0, 1, 1)

        self.lowcondlabel_2 = QLabel(self.cutPara_groupBox)
        self.lowcondlabel_2.setObjectName(u"lowcondlabel_2")
        self.lowcondlabel_2.setFont(font2)

        self.gridLayout.addWidget(self.lowcondlabel_2, 0, 3, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 0, 1, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.sinefrelabel = QLabel(self.cutPara_groupBox)
        self.sinefrelabel.setObjectName(u"sinefrelabel")
        self.sinefrelabel.setFont(font2)

        self.gridLayout_6.addWidget(self.sinefrelabel, 1, 0, 1, 1)

        self.sine_frequence_lineEdit_sine = QLineEdit(self.cutPara_groupBox)
        self.sine_frequence_lineEdit_sine.setObjectName(u"sine_frequence_lineEdit_sine")
        self.sine_frequence_lineEdit_sine.setMinimumSize(QSize(50, 20))
        self.sine_frequence_lineEdit_sine.setMaximumSize(QSize(100, 40))
        self.sine_frequence_lineEdit_sine.setFont(font2)

        self.gridLayout_6.addWidget(self.sine_frequence_lineEdit_sine, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_6, 1, 2, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.square_label_3 = QLabel(self.cutPara_groupBox)
        self.square_label_3.setObjectName(u"square_label_3")
        self.square_label_3.setFont(font2)
        self.square_label_3.setStyleSheet(u"#square_label_3{\n"
"color:rgb(37, 123, 188)\n"
"}")

        self.horizontalLayout_14.addWidget(self.square_label_3)

        self.line_6 = QFrame(self.cutPara_groupBox)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_14.addWidget(self.line_6)

        self.horizontalLayout_14.setStretch(1, 1)

        self.gridLayout_5.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.sine_label_3 = QLabel(self.cutPara_groupBox)
        self.sine_label_3.setObjectName(u"sine_label_3")
        self.sine_label_3.setFont(font2)
        self.sine_label_3.setStyleSheet(u"#sine_label_3{\n"
"color:rgb(125, 102, 140)\n"
"}")

        self.horizontalLayout_11.addWidget(self.sine_label_3)

        self.line_3 = QFrame(self.cutPara_groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_11.addWidget(self.line_3)

        self.horizontalLayout_11.setStretch(1, 1)

        self.gridLayout_5.addLayout(self.horizontalLayout_11, 0, 2, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.squarefrelabel = QLabel(self.cutPara_groupBox)
        self.squarefrelabel.setObjectName(u"squarefrelabel")
        self.squarefrelabel.setFont(font2)

        self.gridLayout_7.addWidget(self.squarefrelabel, 1, 0, 1, 1)

        self.square_frequence_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.square_frequence_lineEdit.setObjectName(u"square_frequence_lineEdit")
        self.square_frequence_lineEdit.setMinimumSize(QSize(50, 20))
        self.square_frequence_lineEdit.setMaximumSize(QSize(100, 40))
        self.square_frequence_lineEdit.setFont(font2)

        self.gridLayout_7.addWidget(self.square_frequence_lineEdit, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_7, 1, 0, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_5)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.square_label_6 = QLabel(self.cutPara_groupBox)
        self.square_label_6.setObjectName(u"square_label_6")
        self.square_label_6.setFont(font2)
        self.square_label_6.setStyleSheet(u"#square_label_6{\n"
"color:rgb(141, 0, 0)\n"
"}")

        self.horizontalLayout_18.addWidget(self.square_label_6)

        self.line_9 = QFrame(self.cutPara_groupBox)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_18.addWidget(self.line_9)

        self.horizontalLayout_18.setStretch(1, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.threlabel = QLabel(self.cutPara_groupBox)
        self.threlabel.setObjectName(u"threlabel")
        self.threlabel.setFont(font2)

        self.gridLayout_10.addWidget(self.threlabel, 1, 0, 1, 1)

        self.threshold_lineEdit = QLineEdit(self.cutPara_groupBox)
        self.threshold_lineEdit.setObjectName(u"threshold_lineEdit")
        self.threshold_lineEdit.setMinimumSize(QSize(50, 20))
        self.threshold_lineEdit.setMaximumSize(QSize(100, 40))
        self.threshold_lineEdit.setFont(font2)

        self.gridLayout_10.addWidget(self.threshold_lineEdit, 1, 1, 1, 1)


        self.horizontalLayout_12.addLayout(self.gridLayout_10)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_12)


        self.verticalLayout_14.addLayout(self.horizontalLayout_12)


        self.verticalLayout_5.addLayout(self.verticalLayout_14)


        self.verticalLayout_9.addWidget(self.cutPara_groupBox)

        self.draw_groupbox = QGroupBox(self.Basic_Set_Tab)
        self.draw_groupbox.setObjectName(u"draw_groupbox")
        self.draw_groupbox.setMinimumSize(QSize(0, 0))
        self.draw_groupbox.setMaximumSize(QSize(16777215, 16777215))
        self.draw_groupbox.setFont(font1)
        self.verticalLayout_4 = QVBoxLayout(self.draw_groupbox)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(3, 6, 3, 3)
        self.tabWidget = QTabWidget(self.draw_groupbox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font1)
        self.Setting_2d = QWidget()
        self.Setting_2d.setObjectName(u"Setting_2d")
        self.verticalLayout_7 = QVBoxLayout(self.Setting_2d)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.color_2d_comboBox = QComboBox(self.Setting_2d)
        self.color_2d_comboBox.setObjectName(u"color_2d_comboBox")
        self.color_2d_comboBox.setMinimumSize(QSize(50, 25))
        self.color_2d_comboBox.setMaximumSize(QSize(100, 40))
        self.color_2d_comboBox.setFont(font2)

        self.gridLayout_4.addWidget(self.color_2d_comboBox, 4, 1, 1, 1)

        self.binxlabel_2d = QLabel(self.Setting_2d)
        self.binxlabel_2d.setObjectName(u"binxlabel_2d")
        self.binxlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.binxlabel_2d, 0, 0, 1, 1)

        self.xmaxlabel_2d = QLabel(self.Setting_2d)
        self.xmaxlabel_2d.setObjectName(u"xmaxlabel_2d")
        self.xmaxlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.xmaxlabel_2d, 2, 3, 1, 1)

        self.colormaplabel_2d = QLabel(self.Setting_2d)
        self.colormaplabel_2d.setObjectName(u"colormaplabel_2d")
        self.colormaplabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.colormaplabel_2d, 4, 0, 1, 1)

        self.gminlabel_2d = QLabel(self.Setting_2d)
        self.gminlabel_2d.setObjectName(u"gminlabel_2d")
        self.gminlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.gminlabel_2d, 1, 3, 1, 1)

        self.xmin_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.xmin_2d_lineEdit.setObjectName(u"xmin_2d_lineEdit")
        self.xmin_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.xmin_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.xmin_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.xmin_2d_lineEdit, 2, 1, 1, 1)

        self.binsy_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.binsy_2d_lineEdit.setObjectName(u"binsy_2d_lineEdit")
        self.binsy_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.binsy_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.binsy_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.binsy_2d_lineEdit, 0, 4, 1, 1)

        self.gmin_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.gmin_2d_lineEdit.setObjectName(u"gmin_2d_lineEdit")
        self.gmin_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.gmin_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.gmin_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.gmin_2d_lineEdit, 1, 4, 1, 1)

        self.cmin_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.cmin_2d_lineEdit.setObjectName(u"cmin_2d_lineEdit")
        self.cmin_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.cmin_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.cmin_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.cmin_2d_lineEdit, 3, 1, 1, 1)

        self.gmax_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.gmax_2d_lineEdit.setObjectName(u"gmax_2d_lineEdit")
        self.gmax_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.gmax_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.gmax_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.gmax_2d_lineEdit, 1, 1, 1, 1)

        self.cminlabel_2d = QLabel(self.Setting_2d)
        self.cminlabel_2d.setObjectName(u"cminlabel_2d")
        self.cminlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.cminlabel_2d, 3, 0, 1, 1)

        self.vmaxlabel_2d = QLabel(self.Setting_2d)
        self.vmaxlabel_2d.setObjectName(u"vmaxlabel_2d")
        self.vmaxlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.vmaxlabel_2d, 3, 3, 1, 1)

        self.xminlabel_2d = QLabel(self.Setting_2d)
        self.xminlabel_2d.setObjectName(u"xminlabel_2d")
        self.xminlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.xminlabel_2d, 2, 0, 1, 1)

        self.xmax_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.xmax_2d_lineEdit.setObjectName(u"xmax_2d_lineEdit")
        self.xmax_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.xmax_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.xmax_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.xmax_2d_lineEdit, 2, 4, 1, 1)

        self.gmaxlabel_2d = QLabel(self.Setting_2d)
        self.gmaxlabel_2d.setObjectName(u"gmaxlabel_2d")
        self.gmaxlabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.gmaxlabel_2d, 1, 0, 1, 1)

        self.binsx_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.binsx_2d_lineEdit.setObjectName(u"binsx_2d_lineEdit")
        self.binsx_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.binsx_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.binsx_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.binsx_2d_lineEdit, 0, 1, 1, 1)

        self.colormax_2d_lineEdit = QLineEdit(self.Setting_2d)
        self.colormax_2d_lineEdit.setObjectName(u"colormax_2d_lineEdit")
        self.colormax_2d_lineEdit.setMinimumSize(QSize(50, 20))
        self.colormax_2d_lineEdit.setMaximumSize(QSize(100, 40))
        self.colormax_2d_lineEdit.setFont(font2)

        self.gridLayout_4.addWidget(self.colormax_2d_lineEdit, 3, 4, 1, 1)

        self.binylabel_2d = QLabel(self.Setting_2d)
        self.binylabel_2d.setObjectName(u"binylabel_2d")
        self.binylabel_2d.setFont(font2)

        self.gridLayout_4.addWidget(self.binylabel_2d, 0, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 2, 2, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_4)

        self.tabWidget.addTab(self.Setting_2d, "")
        self.Setting_1d = QWidget()
        self.Setting_1d.setObjectName(u"Setting_1d")
        self.verticalLayout_2 = QVBoxLayout(self.Setting_1d)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bins_1d_lineEdit = QLineEdit(self.Setting_1d)
        self.bins_1d_lineEdit.setObjectName(u"bins_1d_lineEdit")
        self.bins_1d_lineEdit.setMinimumSize(QSize(50, 20))
        self.bins_1d_lineEdit.setMaximumSize(QSize(100, 40))
        self.bins_1d_lineEdit.setFont(font2)

        self.gridLayout_3.addWidget(self.bins_1d_lineEdit, 0, 1, 1, 1)

        self.binlabel_1d = QLabel(self.Setting_1d)
        self.binlabel_1d.setObjectName(u"binlabel_1d")
        self.binlabel_1d.setFont(font2)

        self.gridLayout_3.addWidget(self.binlabel_1d, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.Setting_1d, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer)

        self.redraw_pushButton = QPushButton(self.draw_groupbox)
        self.redraw_pushButton.setObjectName(u"redraw_pushButton")
        self.redraw_pushButton.setMinimumSize(QSize(50, 25))

        self.horizontalLayout_16.addWidget(self.redraw_pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_9.addWidget(self.draw_groupbox)

        self.logWidget = QWidget(self.Basic_Set_Tab)
        self.logWidget.setObjectName(u"logWidget")
        self.logWidget.setMinimumSize(QSize(0, 0))
        self.logWidget.setMaximumSize(QSize(16777215, 16777215))
        self.logWidget.setSizeIncrement(QSize(0, 0))
        self.verticalLayout_6 = QVBoxLayout(self.logWidget)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(1, 1, 1, 0)

        self.verticalLayout_9.addWidget(self.logWidget)

        self.verticalLayout_9.setStretch(2, 1)

        self.verticalLayout_13.addLayout(self.verticalLayout_9)

        self.para_tabWidget.addTab(self.Basic_Set_Tab, "")
        self.Fitting_Set_Tab = QWidget()
        self.Fitting_Set_Tab.setObjectName(u"Fitting_Set_Tab")
        self.verticalLayout_8 = QVBoxLayout(self.Fitting_Set_Tab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.BasicPara_groupbox = QGroupBox(self.Fitting_Set_Tab)
        self.BasicPara_groupbox.setObjectName(u"BasicPara_groupbox")
        self.BasicPara_groupbox.setMinimumSize(QSize(0, 0))
        self.BasicPara_groupbox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.BasicPara_groupbox)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.a2label = QLabel(self.BasicPara_groupbox)
        self.a2label.setObjectName(u"a2label")
        self.a2label.setFont(font2)

        self.horizontalLayout_5.addWidget(self.a2label)

        self.a2_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.a2_lineEdit.setObjectName(u"a2_lineEdit")
        self.a2_lineEdit.setMinimumSize(QSize(50, 20))
        self.a2_lineEdit.setMaximumSize(QSize(100, 40))
        self.a2_lineEdit.setFont(font2)

        self.horizontalLayout_5.addWidget(self.a2_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.v0label = QLabel(self.BasicPara_groupbox)
        self.v0label.setObjectName(u"v0label")
        self.v0label.setFont(font2)

        self.horizontalLayout.addWidget(self.v0label)

        self.v0_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.v0_lineEdit.setObjectName(u"v0_lineEdit")
        self.v0_lineEdit.setMinimumSize(QSize(50, 20))
        self.v0_lineEdit.setMaximumSize(QSize(100, 40))
        self.v0_lineEdit.setFont(font2)

        self.horizontalLayout.addWidget(self.v0_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.g0label = QLabel(self.BasicPara_groupbox)
        self.g0label.setObjectName(u"g0label")
        self.g0label.setFont(font2)

        self.horizontalLayout_2.addWidget(self.g0label)

        self.g0_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.g0_lineEdit.setObjectName(u"g0_lineEdit")
        self.g0_lineEdit.setMinimumSize(QSize(50, 20))
        self.g0_lineEdit.setMaximumSize(QSize(100, 40))
        self.g0_lineEdit.setFont(font2)

        self.horizontalLayout_2.addWidget(self.g0_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.b1label = QLabel(self.BasicPara_groupbox)
        self.b1label.setObjectName(u"b1label")
        self.b1label.setFont(font2)

        self.horizontalLayout_4.addWidget(self.b1label)

        self.b1_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.b1_lineEdit.setObjectName(u"b1_lineEdit")
        self.b1_lineEdit.setMinimumSize(QSize(50, 20))
        self.b1_lineEdit.setMaximumSize(QSize(100, 40))
        self.b1_lineEdit.setFont(font2)

        self.horizontalLayout_4.addWidget(self.b1_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.b2label = QLabel(self.BasicPara_groupbox)
        self.b2label.setObjectName(u"b2label")
        self.b2label.setFont(font2)

        self.horizontalLayout_6.addWidget(self.b2label)

        self.b2_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.b2_lineEdit.setObjectName(u"b2_lineEdit")
        self.b2_lineEdit.setMinimumSize(QSize(50, 20))
        self.b2_lineEdit.setMaximumSize(QSize(100, 40))
        self.b2_lineEdit.setFont(font2)

        self.horizontalLayout_6.addWidget(self.b2_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.a1label = QLabel(self.BasicPara_groupbox)
        self.a1label.setObjectName(u"a1label")
        self.a1label.setFont(font2)

        self.horizontalLayout_3.addWidget(self.a1label)

        self.a1_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.a1_lineEdit.setObjectName(u"a1_lineEdit")
        self.a1_lineEdit.setMinimumSize(QSize(50, 20))
        self.a1_lineEdit.setMaximumSize(QSize(100, 40))
        self.a1_lineEdit.setFont(font2)

        self.horizontalLayout_3.addWidget(self.a1_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout_8.addWidget(self.BasicPara_groupbox)

        self.verticalSpacer = QSpacerItem(20, 502, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.para_tabWidget.addTab(self.Fitting_Set_Tab, "")

        self.horizontalLayout_7.addWidget(self.para_tabWidget)

        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_12.addLayout(self.horizontalLayout_7)

        BasicanalysisWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(BasicanalysisWindow)
        self.statusbar.setObjectName(u"statusbar")
        BasicanalysisWindow.setStatusBar(self.statusbar)

        self.retranslateUi(BasicanalysisWindow)

        self.draw_stackedWidget.setCurrentIndex(1)
        self.para_tabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(BasicanalysisWindow)
    # setupUi

    def retranslateUi(self, BasicanalysisWindow):
        BasicanalysisWindow.setWindowTitle(QCoreApplication.translate("BasicanalysisWindow", u"Analysis", None))
        self.open_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Open", None))
        self.run_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Run", None))
        self.view_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"View", None))
        self.save_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Save", None))
        self.quit_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Quit", None))
        self.about_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"About", None))
        self.singleselect_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Single", None))
        self.label_20.setText(QCoreApplication.translate("BasicanalysisWindow", u"Log", None))
        self.cutPara_groupBox.setTitle(QCoreApplication.translate("BasicanalysisWindow", u"CutPara", None))
        self.timelabel_2.setText(QCoreApplication.translate("BasicanalysisWindow", u"Time(ms)", None))
        self.time_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"100", None))
        self.highcond_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-1", None))
        self.samplefrelabel.setText(QCoreApplication.translate("BasicanalysisWindow", u"Sample Rate", None))
        self.lowcond_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-5", None))
        self.sample_rate_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"20000", None))
        self.addlenlabel_2.setText(QCoreApplication.translate("BasicanalysisWindow", u"Additional Length", None))
        self.additional_length_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"0", None))
        self.highcondlabel_2.setText(QCoreApplication.translate("BasicanalysisWindow", u"High Cond", None))
        self.lowcondlabel_2.setText(QCoreApplication.translate("BasicanalysisWindow", u"Low Cond", None))
        self.sinefrelabel.setText(QCoreApplication.translate("BasicanalysisWindow", u"Sine Frequence", None))
        self.sine_frequence_lineEdit_sine.setText(QCoreApplication.translate("BasicanalysisWindow", u"100", None))
        self.square_label_3.setText(QCoreApplication.translate("BasicanalysisWindow", u"Bias_square", None))
        self.sine_label_3.setText(QCoreApplication.translate("BasicanalysisWindow", u"Bias_sine", None))
        self.squarefrelabel.setText(QCoreApplication.translate("BasicanalysisWindow", u"Square Frequence", None))
        self.square_frequence_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"20", None))
        self.square_label_6.setText(QCoreApplication.translate("BasicanalysisWindow", u"New Method", None))
        self.threlabel.setText(QCoreApplication.translate("BasicanalysisWindow", u"Threshold", None))
        self.threshold_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"20", None))
        self.draw_groupbox.setTitle(QCoreApplication.translate("BasicanalysisWindow", u"DrawPara", None))
        self.binxlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"BinsX", None))
        self.xmaxlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"X_Max", None))
        self.colormaplabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"ColorMap", None))
        self.gminlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"G_Min", None))
        self.xmin_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-10", None))
        self.binsy_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"200", None))
        self.gmin_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-6", None))
        self.cmin_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"0", None))
        self.gmax_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-1.5", None))
        self.cminlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"Counts Min", None))
        self.vmaxlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"Color Max", None))
        self.xminlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"X_Min", None))
        self.xmax_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-10", None))
        self.gmaxlabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"G_Max", None))
        self.binsx_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"200", None))
        self.colormax_2d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"0", None))
        self.binylabel_2d.setText(QCoreApplication.translate("BasicanalysisWindow", u"BinsY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Setting_2d), QCoreApplication.translate("BasicanalysisWindow", u"2D Plotting", None))
        self.bins_1d_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"500", None))
        self.binlabel_1d.setText(QCoreApplication.translate("BasicanalysisWindow", u"1D Bins", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Setting_1d), QCoreApplication.translate("BasicanalysisWindow", u"1D Plotting", None))
        self.redraw_pushButton.setText(QCoreApplication.translate("BasicanalysisWindow", u"Redraw", None))
        self.para_tabWidget.setTabText(self.para_tabWidget.indexOf(self.Basic_Set_Tab), QCoreApplication.translate("BasicanalysisWindow", u"Basic_Set", None))
        self.BasicPara_groupbox.setTitle(QCoreApplication.translate("BasicanalysisWindow", u"BasicPara", None))
        self.a2label.setText(QCoreApplication.translate("BasicanalysisWindow", u"a2", None))
        self.a2_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-4.1044", None))
        self.v0label.setText(QCoreApplication.translate("BasicanalysisWindow", u"V0", None))
        self.v0_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"0.1", None))
        self.g0label.setText(QCoreApplication.translate("BasicanalysisWindow", u"G0", None))
        self.g0_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"12.9", None))
        self.b1label.setText(QCoreApplication.translate("BasicanalysisWindow", u"b1", None))
        self.b1_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-13.196", None))
        self.b2label.setText(QCoreApplication.translate("BasicanalysisWindow", u"b2", None))
        self.b2_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"-13.135", None))
        self.a1label.setText(QCoreApplication.translate("BasicanalysisWindow", u"a1", None))
        self.a1_lineEdit.setText(QCoreApplication.translate("BasicanalysisWindow", u"4.1422", None))
        self.para_tabWidget.setTabText(self.para_tabWidget.indexOf(self.Fitting_Set_Tab), QCoreApplication.translate("BasicanalysisWindow", u"Fitting_Set", None))
    # retranslateUi

