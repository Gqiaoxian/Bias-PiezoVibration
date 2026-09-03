# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Piezo_Para.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(420, 109)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.square_label_6 = QLabel(Form)
        self.square_label_6.setObjectName(u"square_label_6")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.square_label_6.setFont(font)
        self.square_label_6.setStyleSheet(u"#square_label_6\n"
"{\n"
"color:rgb(99, 134, 77)\n"
"}")

        self.horizontalLayout_34.addWidget(self.square_label_6)

        self.line_9 = QFrame(Form)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_34.addWidget(self.line_9)

        self.horizontalLayout_34.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_34)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.highcondlabel = QLabel(Form)
        self.highcondlabel.setObjectName(u"highcondlabel")

        self.horizontalLayout_2.addWidget(self.highcondlabel)

        self.piezo_highcond_lineEdit = QLineEdit(Form)
        self.piezo_highcond_lineEdit.setObjectName(u"piezo_highcond_lineEdit")
        self.piezo_highcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.piezo_highcond_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_2.addWidget(self.piezo_highcond_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lowcondlabel = QLabel(Form)
        self.lowcondlabel.setObjectName(u"lowcondlabel")

        self.horizontalLayout.addWidget(self.lowcondlabel)

        self.piezo_lowcond_lineEdit = QLineEdit(Form)
        self.piezo_lowcond_lineEdit.setObjectName(u"piezo_lowcond_lineEdit")
        self.piezo_lowcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.piezo_lowcond_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.piezo_lowcond_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 1)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.lowlenlabel = QLabel(Form)
        self.lowlenlabel.setObjectName(u"lowlenlabel")

        self.horizontalLayout_35.addWidget(self.lowlenlabel)

        self.lenlow_lineEdit = QLineEdit(Form)
        self.lenlow_lineEdit.setObjectName(u"lenlow_lineEdit")
        self.lenlow_lineEdit.setMinimumSize(QSize(50, 20))
        self.lenlow_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_35.addWidget(self.lenlow_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_35, 1, 2, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.highlenlabel = QLabel(Form)
        self.highlenlabel.setObjectName(u"highlenlabel")

        self.horizontalLayout_10.addWidget(self.highlenlabel)

        self.lenhigh_lineEdit = QLineEdit(Form)
        self.lenhigh_lineEdit.setObjectName(u"lenhigh_lineEdit")
        self.lenhigh_lineEdit.setMinimumSize(QSize(50, 20))
        self.lenhigh_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_10.addWidget(self.lenhigh_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.square_label_6.setText(QCoreApplication.translate("Form", u"Piezo Calibration ", None))
        self.highcondlabel.setText(QCoreApplication.translate("Form", u"HIGH COND", None))
        self.piezo_highcond_lineEdit.setText(QCoreApplication.translate("Form", u"-1", None))
        self.lowcondlabel.setText(QCoreApplication.translate("Form", u"LOW COND", None))
        self.piezo_lowcond_lineEdit.setText(QCoreApplication.translate("Form", u"-5", None))
        self.lowlenlabel.setText(QCoreApplication.translate("Form", u"LOW LEN", None))
        self.lenlow_lineEdit.setText(QCoreApplication.translate("Form", u"-5", None))
        self.highlenlabel.setText(QCoreApplication.translate("Form", u"HIGH LEN", None))
        self.lenhigh_lineEdit.setText(QCoreApplication.translate("Form", u"-1", None))
    # retranslateUi

