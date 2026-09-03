# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'singletrace.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)
import ui.images_rc

class Ui_singletrace(object):
    def setupUi(self, singletrace):
        if not singletrace.objectName():
            singletrace.setObjectName(u"singletrace")
        singletrace.resize(907, 645)
        self.centralwidget = QWidget(singletrace)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.open_pushButton = QToolButton(self.centralwidget)
        self.open_pushButton.setObjectName(u"open_pushButton")
        self.open_pushButton.setMinimumSize(QSize(60, 40))
        self.open_pushButton.setMaximumSize(QSize(80, 16777215))
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        self.open_pushButton.setFont(font)
        icon = QIcon()
        icon.addFile(u":/png/images/openfile.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_pushButton.setIcon(icon)
        self.open_pushButton.setIconSize(QSize(20, 20))
        self.open_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_3.addWidget(self.open_pushButton)

        self.save_pushButton = QToolButton(self.centralwidget)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setMinimumSize(QSize(60, 40))
        self.save_pushButton.setMaximumSize(QSize(80, 16777215))
        self.save_pushButton.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/png/images/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_pushButton.setIcon(icon1)
        self.save_pushButton.setIconSize(QSize(20, 20))
        self.save_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout_3.addWidget(self.save_pushButton)

        self.Select_all_checkBox = QCheckBox(self.centralwidget)
        self.Select_all_checkBox.setObjectName(u"Select_all_checkBox")

        self.horizontalLayout_3.addWidget(self.Select_all_checkBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftpushButton = QPushButton(self.groupBox)
        self.leftpushButton.setObjectName(u"leftpushButton")
        self.leftpushButton.setMinimumSize(QSize(30, 30))
        self.leftpushButton.setMaximumSize(QSize(35, 35))
        self.leftpushButton.setSizeIncrement(QSize(0, 0))
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.leftpushButton.setIcon(icon2)
        self.leftpushButton.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.leftpushButton)

        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout.addWidget(self.widget)

        self.rightpushButton = QPushButton(self.groupBox)
        self.rightpushButton.setObjectName(u"rightpushButton")
        self.rightpushButton.setMinimumSize(QSize(30, 30))
        self.rightpushButton.setMaximumSize(QSize(35, 35))
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.rightpushButton.setIcon(icon3)
        self.rightpushButton.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.rightpushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tracenumlabel = QLabel(self.groupBox_2)
        self.tracenumlabel.setObjectName(u"tracenumlabel")

        self.horizontalLayout_4.addWidget(self.tracenumlabel)

        self.tracenum_lineEdit = QLineEdit(self.groupBox_2)
        self.tracenum_lineEdit.setObjectName(u"tracenum_lineEdit")
        self.tracenum_lineEdit.setMinimumSize(QSize(50, 20))
        self.tracenum_lineEdit.setMaximumSize(QSize(100, 40))
        self.tracenum_lineEdit.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.tracenum_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.chosennumlabel = QLabel(self.groupBox_2)
        self.chosennumlabel.setObjectName(u"chosennumlabel")

        self.horizontalLayout_5.addWidget(self.chosennumlabel)

        self.chosennum_lineEdit = QLineEdit(self.groupBox_2)
        self.chosennum_lineEdit.setObjectName(u"chosennum_lineEdit")
        self.chosennum_lineEdit.setMinimumSize(QSize(50, 20))
        self.chosennum_lineEdit.setMaximumSize(QSize(100, 40))
        self.chosennum_lineEdit.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.chosennum_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.curindexlabel = QLabel(self.groupBox_2)
        self.curindexlabel.setObjectName(u"curindexlabel")

        self.horizontalLayout_6.addWidget(self.curindexlabel)

        self.curindex_lineEdit = QLineEdit(self.groupBox_2)
        self.curindex_lineEdit.setObjectName(u"curindex_lineEdit")
        self.curindex_lineEdit.setMinimumSize(QSize(50, 20))
        self.curindex_lineEdit.setMaximumSize(QSize(100, 40))
        self.curindex_lineEdit.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.curindex_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.npzButton = QRadioButton(self.groupBox_3)
        self.npzButton.setObjectName(u"npzButton")
        self.npzButton.setChecked(True)

        self.verticalLayout_2.addWidget(self.npzButton)

        self.csvButton = QRadioButton(self.groupBox_3)
        self.csvButton.setObjectName(u"csvButton")

        self.verticalLayout_2.addWidget(self.csvButton)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.bias_checkBox = QCheckBox(self.groupBox_4)
        self.bias_checkBox.setObjectName(u"bias_checkBox")
        self.bias_checkBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.bias_checkBox)

        self.log_checkBox = QCheckBox(self.groupBox_4)
        self.log_checkBox.setObjectName(u"log_checkBox")
        self.log_checkBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.log_checkBox)

        self.peak_checkBox = QCheckBox(self.groupBox_4)
        self.peak_checkBox.setObjectName(u"peak_checkBox")
        self.peak_checkBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.peak_checkBox)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.redrawpushButton = QPushButton(self.centralwidget)
        self.redrawpushButton.setObjectName(u"redrawpushButton")

        self.verticalLayout_5.addWidget(self.redrawpushButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.verticalLayout_6.setStretch(1, 1)
        singletrace.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(singletrace)
        self.statusbar.setObjectName(u"statusbar")
        singletrace.setStatusBar(self.statusbar)

        self.retranslateUi(singletrace)

        QMetaObject.connectSlotsByName(singletrace)
    # setupUi

    def retranslateUi(self, singletrace):
        singletrace.setWindowTitle(QCoreApplication.translate("singletrace", u"MainWindow", None))
        self.open_pushButton.setText(QCoreApplication.translate("singletrace", u"Open", None))
        self.save_pushButton.setText(QCoreApplication.translate("singletrace", u"Save", None))
        self.Select_all_checkBox.setText(QCoreApplication.translate("singletrace", u"Select All", None))
        self.groupBox.setTitle(QCoreApplication.translate("singletrace", u"Single Trace", None))
        self.leftpushButton.setText("")
        self.rightpushButton.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("singletrace", u"Status", None))
        self.tracenumlabel.setText(QCoreApplication.translate("singletrace", u"Trace Nums", None))
        self.tracenum_lineEdit.setText(QCoreApplication.translate("singletrace", u"0", None))
        self.chosennumlabel.setText(QCoreApplication.translate("singletrace", u"Chosen Nums", None))
        self.chosennum_lineEdit.setText(QCoreApplication.translate("singletrace", u"0", None))
        self.curindexlabel.setText(QCoreApplication.translate("singletrace", u"Cur Index", None))
        self.curindex_lineEdit.setText(QCoreApplication.translate("singletrace", u"0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("singletrace", u"Save Setting", None))
        self.npzButton.setText(QCoreApplication.translate("singletrace", u"npz", None))
        self.csvButton.setText(QCoreApplication.translate("singletrace", u"csv", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("singletrace", u"View Setting", None))
        self.bias_checkBox.setText(QCoreApplication.translate("singletrace", u"Bias", None))
        self.log_checkBox.setText(QCoreApplication.translate("singletrace", u"Log(G/G0)", None))
        self.peak_checkBox.setText(QCoreApplication.translate("singletrace", u"Peak", None))
        self.redrawpushButton.setText(QCoreApplication.translate("singletrace", u"Redraw", None))
    # retranslateUi

