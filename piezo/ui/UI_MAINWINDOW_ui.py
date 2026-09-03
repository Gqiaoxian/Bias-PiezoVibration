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
    QSpacerItem, QStackedWidget, QStatusBar, QTextBrowser,
    QToolButton, QVBoxLayout, QWidget)
import ui.images_rc

class Ui_basicanalysiswindow(object):
    def setupUi(self, basicanalysiswindow):
        if not basicanalysiswindow.objectName():
            basicanalysiswindow.setObjectName(u"basicanalysiswindow")
        basicanalysiswindow.resize(1351, 850)
        self.centralwidget = QWidget(basicanalysiswindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_14 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setSpacing(3)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.stackedWidget_button = QStackedWidget(self.centralwidget)
        self.stackedWidget_button.setObjectName(u"stackedWidget_button")
        self.stackedWidget_button.setMaximumSize(QSize(188, 16777215))
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget_button.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stackedWidget_button.addWidget(self.page_4)

        self.horizontalLayout_25.addWidget(self.stackedWidget_button)

        self.quit_pushButton = QToolButton(self.centralwidget)
        self.quit_pushButton.setObjectName(u"quit_pushButton")
        self.quit_pushButton.setMinimumSize(QSize(60, 40))
        self.quit_pushButton.setMaximumSize(QSize(80, 16777215))
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        self.quit_pushButton.setFont(font)
        icon = QIcon()
        icon.addFile(u":/png/images/quit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.quit_pushButton.setIcon(icon)
        self.quit_pushButton.setIconSize(QSize(20, 20))
        self.quit_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_25.addWidget(self.quit_pushButton)

        self.about_pushButton = QToolButton(self.centralwidget)
        self.about_pushButton.setObjectName(u"about_pushButton")
        self.about_pushButton.setMinimumSize(QSize(60, 40))
        self.about_pushButton.setMaximumSize(QSize(80, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        self.about_pushButton.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/png/images/about.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.about_pushButton.setIcon(icon1)
        self.about_pushButton.setIconSize(QSize(20, 20))
        self.about_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_25.addWidget(self.about_pushButton)

        self.singleFilter_pushButton = QToolButton(self.centralwidget)
        self.singleFilter_pushButton.setObjectName(u"singleFilter_pushButton")
        self.singleFilter_pushButton.setMinimumSize(QSize(60, 40))
        self.singleFilter_pushButton.setMaximumSize(QSize(80, 16777215))
        self.singleFilter_pushButton.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/png/images/select.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.singleFilter_pushButton.setIcon(icon2)
        self.singleFilter_pushButton.setIconSize(QSize(20, 20))
        self.singleFilter_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_25.addWidget(self.singleFilter_pushButton)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(150, 40))
        self.comboBox.setMaximumSize(QSize(200, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.comboBox.setFont(font2)

        self.horizontalLayout_25.addWidget(self.comboBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_3)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_25.addWidget(self.progressBar)

        self.horizontalLayout_25.setStretch(4, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout_25)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(600, 0))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_10.addWidget(self.stackedWidget)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(1, -1, 1, 0)
        self.label_20 = QLabel(self.widget)
        self.label_20.setObjectName(u"label_20")
        font3 = QFont()
        font3.setBold(False)
        self.label_20.setFont(font3)

        self.verticalLayout_6.addWidget(self.label_20)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_6.addWidget(self.textBrowser)

        self.verticalLayout_6.setStretch(1, 1)

        self.verticalLayout_10.addWidget(self.widget)

        self.verticalLayout_10.setStretch(0, 2)
        self.verticalLayout_10.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_10)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.draw_groupbox = QGroupBox(self.centralwidget)
        self.draw_groupbox.setObjectName(u"draw_groupbox")
        self.verticalLayout_4 = QVBoxLayout(self.draw_groupbox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.BasicPara_groupbox = QGroupBox(self.draw_groupbox)
        self.BasicPara_groupbox.setObjectName(u"BasicPara_groupbox")
        self.verticalLayout_8 = QVBoxLayout(self.BasicPara_groupbox)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.square_label_8 = QLabel(self.BasicPara_groupbox)
        self.square_label_8.setObjectName(u"square_label_8")
        self.square_label_8.setFont(font2)
        self.square_label_8.setStyleSheet(u"#square_label_6\n"
"{\n"
"color:rgb(99, 134, 77)\n"
"}")

        self.horizontalLayout_26.addWidget(self.square_label_8)

        self.line_11 = QFrame(self.BasicPara_groupbox)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_26.addWidget(self.line_11)

        self.horizontalLayout_26.setStretch(1, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_26)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 1, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.a1label = QLabel(self.BasicPara_groupbox)
        self.a1label.setObjectName(u"a1label")

        self.horizontalLayout_3.addWidget(self.a1label)

        self.a1_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.a1_lineEdit.setObjectName(u"a1_lineEdit")
        self.a1_lineEdit.setMinimumSize(QSize(50, 20))
        self.a1_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_3.addWidget(self.a1_lineEdit)


        self.gridLayout_4.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.b1label = QLabel(self.BasicPara_groupbox)
        self.b1label.setObjectName(u"b1label")

        self.horizontalLayout_4.addWidget(self.b1label)

        self.b1_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.b1_lineEdit.setObjectName(u"b1_lineEdit")
        self.b1_lineEdit.setMinimumSize(QSize(50, 20))
        self.b1_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_4.addWidget(self.b1_lineEdit)


        self.gridLayout_4.addLayout(self.horizontalLayout_4, 1, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.a2label = QLabel(self.BasicPara_groupbox)
        self.a2label.setObjectName(u"a2label")

        self.horizontalLayout_5.addWidget(self.a2label)

        self.a2_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.a2_lineEdit.setObjectName(u"a2_lineEdit")
        self.a2_lineEdit.setMinimumSize(QSize(50, 20))
        self.a2_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_5.addWidget(self.a2_lineEdit)


        self.gridLayout_4.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.b2label = QLabel(self.BasicPara_groupbox)
        self.b2label.setObjectName(u"b2label")

        self.horizontalLayout_6.addWidget(self.b2label)

        self.b2_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.b2_lineEdit.setObjectName(u"b2_lineEdit")
        self.b2_lineEdit.setMinimumSize(QSize(50, 20))
        self.b2_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_6.addWidget(self.b2_lineEdit)


        self.gridLayout_4.addLayout(self.horizontalLayout_6, 2, 2, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.vlabel = QLabel(self.BasicPara_groupbox)
        self.vlabel.setObjectName(u"vlabel")

        self.horizontalLayout_7.addWidget(self.vlabel)

        self.V0_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.V0_lineEdit.setObjectName(u"V0_lineEdit")
        self.V0_lineEdit.setMinimumSize(QSize(50, 20))
        self.V0_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_7.addWidget(self.V0_lineEdit)


        self.gridLayout_4.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)


        self.verticalLayout_9.addLayout(self.gridLayout_4)


        self.verticalLayout_8.addLayout(self.verticalLayout_9)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.square_label_9 = QLabel(self.BasicPara_groupbox)
        self.square_label_9.setObjectName(u"square_label_9")
        self.square_label_9.setFont(font2)
        self.square_label_9.setStyleSheet(u"#square_label_9\n"
"{\n"
"color:rgb(131, 0, 0)\n"
"}")

        self.horizontalLayout_30.addWidget(self.square_label_9)

        self.line_12 = QFrame(self.BasicPara_groupbox)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.Shape.HLine)
        self.line_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_30.addWidget(self.line_12)

        self.horizontalLayout_30.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_30)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.piezofrelabel = QLabel(self.BasicPara_groupbox)
        self.piezofrelabel.setObjectName(u"piezofrelabel")

        self.horizontalLayout_13.addWidget(self.piezofrelabel)

        self.hover_frequence_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.hover_frequence_lineEdit.setObjectName(u"hover_frequence_lineEdit")
        self.hover_frequence_lineEdit.setMinimumSize(QSize(50, 20))
        self.hover_frequence_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_13.addWidget(self.hover_frequence_lineEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 1, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.samplefrelabel = QLabel(self.BasicPara_groupbox)
        self.samplefrelabel.setObjectName(u"samplefrelabel")

        self.horizontalLayout_14.addWidget(self.samplefrelabel)

        self.sample_frequence_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.sample_frequence_lineEdit.setObjectName(u"sample_frequence_lineEdit")
        self.sample_frequence_lineEdit.setMinimumSize(QSize(50, 20))
        self.sample_frequence_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_14.addWidget(self.sample_frequence_lineEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.timelabel = QLabel(self.BasicPara_groupbox)
        self.timelabel.setObjectName(u"timelabel")

        self.horizontalLayout_31.addWidget(self.timelabel)

        self.time_lineEdit = QLineEdit(self.BasicPara_groupbox)
        self.time_lineEdit.setObjectName(u"time_lineEdit")
        self.time_lineEdit.setMinimumSize(QSize(50, 20))
        self.time_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_31.addWidget(self.time_lineEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_31, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_5)


        self.verticalLayout_8.addLayout(self.verticalLayout)

        self.Para_stackedWidget = QStackedWidget(self.BasicPara_groupbox)
        self.Para_stackedWidget.setObjectName(u"Para_stackedWidget")
        self.Para_stackedWidget.setMinimumSize(QSize(0, 200))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.Para_stackedWidget.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.Para_stackedWidget.addWidget(self.page_6)

        self.verticalLayout_8.addWidget(self.Para_stackedWidget)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")

        self.verticalLayout_8.addLayout(self.verticalLayout_11)


        self.verticalLayout_4.addWidget(self.BasicPara_groupbox)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_2 = QGroupBox(self.draw_groupbox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 3)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.colormaplabel = QLabel(self.groupBox_2)
        self.colormaplabel.setObjectName(u"colormaplabel")

        self.horizontalLayout_15.addWidget(self.colormaplabel)

        self.color_comboBox = QComboBox(self.groupBox_2)
        self.color_comboBox.setObjectName(u"color_comboBox")
        self.color_comboBox.setMinimumSize(QSize(50, 20))
        self.color_comboBox.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_15.addWidget(self.color_comboBox)


        self.gridLayout_2.addLayout(self.horizontalLayout_15, 3, 2, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.gmaxlabel = QLabel(self.groupBox_2)
        self.gmaxlabel.setObjectName(u"gmaxlabel")

        self.horizontalLayout_20.addWidget(self.gmaxlabel)

        self.G_max_lineEdit = QLineEdit(self.groupBox_2)
        self.G_max_lineEdit.setObjectName(u"G_max_lineEdit")
        self.G_max_lineEdit.setMinimumSize(QSize(50, 20))
        self.G_max_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_20.addWidget(self.G_max_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_20, 1, 0, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.binxlabel = QLabel(self.groupBox_2)
        self.binxlabel.setObjectName(u"binxlabel")

        self.horizontalLayout_18.addWidget(self.binxlabel)

        self.binsx_lineEdit = QLineEdit(self.groupBox_2)
        self.binsx_lineEdit.setObjectName(u"binsx_lineEdit")
        self.binsx_lineEdit.setMinimumSize(QSize(50, 20))
        self.binsx_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_18.addWidget(self.binsx_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_18, 0, 0, 1, 1)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.vmaxlabel = QLabel(self.groupBox_2)
        self.vmaxlabel.setObjectName(u"vmaxlabel")

        self.horizontalLayout_28.addWidget(self.vmaxlabel)

        self.colormax_lineEdit = QLineEdit(self.groupBox_2)
        self.colormax_lineEdit.setObjectName(u"colormax_lineEdit")
        self.colormax_lineEdit.setMinimumSize(QSize(50, 20))
        self.colormax_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_28.addWidget(self.colormax_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_28, 4, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 1, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.gminlabel = QLabel(self.groupBox_2)
        self.gminlabel.setObjectName(u"gminlabel")

        self.horizontalLayout_21.addWidget(self.gminlabel)

        self.G_min_lineEdit = QLineEdit(self.groupBox_2)
        self.G_min_lineEdit.setObjectName(u"G_min_lineEdit")
        self.G_min_lineEdit.setMinimumSize(QSize(50, 20))
        self.G_min_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_21.addWidget(self.G_min_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_21, 1, 2, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.binylabel = QLabel(self.groupBox_2)
        self.binylabel.setObjectName(u"binylabel")

        self.horizontalLayout_19.addWidget(self.binylabel)

        self.binsy_lineEdit = QLineEdit(self.groupBox_2)
        self.binsy_lineEdit.setObjectName(u"binsy_lineEdit")
        self.binsy_lineEdit.setMinimumSize(QSize(50, 20))
        self.binsy_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_19.addWidget(self.binsy_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_19, 0, 2, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.dbinlabel = QLabel(self.groupBox_2)
        self.dbinlabel.setObjectName(u"dbinlabel")

        self.horizontalLayout_17.addWidget(self.dbinlabel)

        self.d1bins_lineEdit = QLineEdit(self.groupBox_2)
        self.d1bins_lineEdit.setObjectName(u"d1bins_lineEdit")
        self.d1bins_lineEdit.setMinimumSize(QSize(50, 20))
        self.d1bins_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_17.addWidget(self.d1bins_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_17, 3, 0, 1, 1)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.cminlabel = QLabel(self.groupBox_2)
        self.cminlabel.setObjectName(u"cminlabel")

        self.horizontalLayout_27.addWidget(self.cminlabel)

        self.cmin_lineEdit = QLineEdit(self.groupBox_2)
        self.cmin_lineEdit.setObjectName(u"cmin_lineEdit")
        self.cmin_lineEdit.setMinimumSize(QSize(50, 20))
        self.cmin_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_27.addWidget(self.cmin_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_27, 4, 0, 1, 1)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.xmaxlabel = QLabel(self.groupBox_2)
        self.xmaxlabel.setObjectName(u"xmaxlabel")

        self.horizontalLayout_37.addWidget(self.xmaxlabel)

        self.x_2d_max_lineEdit = QLineEdit(self.groupBox_2)
        self.x_2d_max_lineEdit.setObjectName(u"x_2d_max_lineEdit")
        self.x_2d_max_lineEdit.setMinimumSize(QSize(50, 20))
        self.x_2d_max_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_37.addWidget(self.x_2d_max_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_37, 2, 2, 1, 1)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.xmin2dlabel = QLabel(self.groupBox_2)
        self.xmin2dlabel.setObjectName(u"xmin2dlabel")

        self.horizontalLayout_38.addWidget(self.xmin2dlabel)

        self.x_2d_min_lineEdit = QLineEdit(self.groupBox_2)
        self.x_2d_min_lineEdit.setObjectName(u"x_2d_min_lineEdit")
        self.x_2d_min_lineEdit.setMinimumSize(QSize(50, 20))
        self.x_2d_min_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_38.addWidget(self.x_2d_min_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_38, 2, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(2, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.draw_groupbox)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, 3)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.pbinslabel = QLabel(self.groupBox)
        self.pbinslabel.setObjectName(u"pbinslabel")

        self.horizontalLayout_29.addWidget(self.pbinslabel)

        self.pbins_lineEdit = QLineEdit(self.groupBox)
        self.pbins_lineEdit.setObjectName(u"pbins_lineEdit")
        self.pbins_lineEdit.setMinimumSize(QSize(50, 20))
        self.pbins_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_29.addWidget(self.pbins_lineEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_29, 1, 0, 1, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.pxminlabel = QLabel(self.groupBox)
        self.pxminlabel.setObjectName(u"pxminlabel")

        self.horizontalLayout_23.addWidget(self.pxminlabel)

        self.xl_lineEdit = QLineEdit(self.groupBox)
        self.xl_lineEdit.setObjectName(u"xl_lineEdit")
        self.xl_lineEdit.setMinimumSize(QSize(50, 20))
        self.xl_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_23.addWidget(self.xl_lineEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_23, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.pxmaxlabel = QLabel(self.groupBox)
        self.pxmaxlabel.setObjectName(u"pxmaxlabel")

        self.horizontalLayout_24.addWidget(self.pxmaxlabel)

        self.xh_lineEdit = QLineEdit(self.groupBox)
        self.xh_lineEdit.setObjectName(u"xh_lineEdit")
        self.xh_lineEdit.setMinimumSize(QSize(50, 20))
        self.xh_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_24.addWidget(self.xh_lineEdit)


        self.gridLayout_3.addLayout(self.horizontalLayout_24, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 0, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(2, 1)

        self.verticalLayout_5.addLayout(self.gridLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_7.addWidget(self.draw_groupbox)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout)

        self.verticalLayout_14.setStretch(1, 1)
        basicanalysiswindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(basicanalysiswindow)
        self.statusbar.setObjectName(u"statusbar")
        basicanalysiswindow.setStatusBar(self.statusbar)

        self.retranslateUi(basicanalysiswindow)

        self.stackedWidget_button.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(basicanalysiswindow)
    # setupUi

    def retranslateUi(self, basicanalysiswindow):
        basicanalysiswindow.setWindowTitle(QCoreApplication.translate("basicanalysiswindow", u"Analysis", None))
        self.quit_pushButton.setText(QCoreApplication.translate("basicanalysiswindow", u"Quit", None))
        self.about_pushButton.setText(QCoreApplication.translate("basicanalysiswindow", u"About", None))
        self.singleFilter_pushButton.setText(QCoreApplication.translate("basicanalysiswindow", u"SingleFilter", None))
        self.label_20.setText(QCoreApplication.translate("basicanalysiswindow", u"Log", None))
        self.draw_groupbox.setTitle(QCoreApplication.translate("basicanalysiswindow", u"DrawPara", None))
        self.BasicPara_groupbox.setTitle(QCoreApplication.translate("basicanalysiswindow", u"BasicPara", None))
        self.square_label_8.setText(QCoreApplication.translate("basicanalysiswindow", u"FitSetting", None))
        self.a1label.setText(QCoreApplication.translate("basicanalysiswindow", u"a1", None))
        self.a1_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"4.1422", None))
        self.b1label.setText(QCoreApplication.translate("basicanalysiswindow", u"b1", None))
        self.b1_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-13.196", None))
        self.a2label.setText(QCoreApplication.translate("basicanalysiswindow", u"a2", None))
        self.a2_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-4.1044", None))
        self.b2label.setText(QCoreApplication.translate("basicanalysiswindow", u"b2", None))
        self.b2_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-13.135", None))
        self.vlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"V0", None))
        self.V0_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"0.1", None))
        self.square_label_9.setText(QCoreApplication.translate("basicanalysiswindow", u"Basic Para", None))
        self.piezofrelabel.setText(QCoreApplication.translate("basicanalysiswindow", u"hover frequence", None))
        self.hover_frequence_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"10", None))
        self.samplefrelabel.setText(QCoreApplication.translate("basicanalysiswindow", u"sample frequence", None))
        self.sample_frequence_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"20000", None))
        self.timelabel.setText(QCoreApplication.translate("basicanalysiswindow", u"Time(ms)", None))
        self.time_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"400", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("basicanalysiswindow", u"Vibration", None))
        self.colormaplabel.setText(QCoreApplication.translate("basicanalysiswindow", u"ColorMap", None))
        self.gmaxlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"G_Max", None))
        self.G_max_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-1.5", None))
        self.binxlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"BinsX", None))
        self.binsx_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"200", None))
        self.vmaxlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"Color Max", None))
        self.colormax_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"0", None))
        self.gminlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"G_Min", None))
        self.G_min_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-6", None))
        self.binylabel.setText(QCoreApplication.translate("basicanalysiswindow", u"BinsY", None))
        self.binsy_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"200", None))
        self.dbinlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"1D Bins", None))
        self.d1bins_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"500", None))
        self.cminlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"Counts Min", None))
        self.cmin_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"10", None))
        self.xmaxlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"X_Max", None))
        self.x_2d_max_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-10", None))
        self.xmin2dlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"X_Min", None))
        self.x_2d_min_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"-10", None))
        self.groupBox.setTitle(QCoreApplication.translate("basicanalysiswindow", u"Piezo Calibration", None))
        self.pbinslabel.setText(QCoreApplication.translate("basicanalysiswindow", u"Bins", None))
        self.pbins_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"100", None))
        self.pxminlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"PiezoX_Min", None))
        self.xl_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"0", None))
        self.pxmaxlabel.setText(QCoreApplication.translate("basicanalysiswindow", u"PiezoX_Max", None))
        self.xh_lineEdit.setText(QCoreApplication.translate("basicanalysiswindow", u"0.045", None))
        self.redraw_pushButton.setText(QCoreApplication.translate("basicanalysiswindow", u"Redraw", None))
    # retranslateUi

