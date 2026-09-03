# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Cut_Para.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(540, 189)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.square_label_7 = QLabel(Form)
        self.square_label_7.setObjectName(u"square_label_7")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.square_label_7.setFont(font)
        self.square_label_7.setStyleSheet(u"#square_label_7{\n"
"color:rgb(105, 80, 117)\n"
"}")

        self.horizontalLayout_36.addWidget(self.square_label_7)

        self.line_10 = QFrame(Form)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_36.addWidget(self.line_10)

        self.horizontalLayout_36.setStretch(1, 1)

        self.verticalLayout_13.addLayout(self.horizontalLayout_36)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.peaknumlabel = QLabel(Form)
        self.peaknumlabel.setObjectName(u"peaknumlabel")

        self.horizontalLayout_9.addWidget(self.peaknumlabel)

        self.peaknum_lineEdit = QLineEdit(Form)
        self.peaknum_lineEdit.setObjectName(u"peaknum_lineEdit")
        self.peaknum_lineEdit.setMinimumSize(QSize(50, 20))
        self.peaknum_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_9.addWidget(self.peaknum_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_12, 1, 1, 1, 1)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.amplitudelabel = QLabel(Form)
        self.amplitudelabel.setObjectName(u"amplitudelabel")

        self.horizontalLayout_40.addWidget(self.amplitudelabel)

        self.hoveramplitude_lineEdit = QLineEdit(Form)
        self.hoveramplitude_lineEdit.setObjectName(u"hoveramplitude_lineEdit")
        self.hoveramplitude_lineEdit.setMinimumSize(QSize(50, 20))
        self.hoveramplitude_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_40.addWidget(self.hoveramplitude_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_40, 0, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.interceplabel = QLabel(Form)
        self.interceplabel.setObjectName(u"interceplabel")

        self.horizontalLayout_7.addWidget(self.interceplabel)

        self.threshold_lineEdit = QLineEdit(Form)
        self.threshold_lineEdit.setObjectName(u"threshold_lineEdit")
        self.threshold_lineEdit.setMinimumSize(QSize(50, 20))
        self.threshold_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_7.addWidget(self.threshold_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.sine1dlabel = QLabel(Form)
        self.sine1dlabel.setObjectName(u"sine1dlabel")

        self.horizontalLayout_12.addWidget(self.sine1dlabel)

        self.length1dfit_lineEdit = QLineEdit(Form)
        self.length1dfit_lineEdit.setObjectName(u"length1dfit_lineEdit")
        self.length1dfit_lineEdit.setMinimumSize(QSize(50, 20))
        self.length1dfit_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_12.addWidget(self.length1dfit_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_12, 1, 2, 1, 1)


        self.verticalLayout_13.addLayout(self.gridLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout_13)

        self.range_open_checkBox = QCheckBox(Form)
        self.range_open_checkBox.setObjectName(u"range_open_checkBox")

        self.verticalLayout_2.addWidget(self.range_open_checkBox)

        self.cond_range_groupBox = QGroupBox(Form)
        self.cond_range_groupBox.setObjectName(u"cond_range_groupBox")
        self.cond_range_groupBox.setStyleSheet(u"#cond_range_groupBox{\\ncolor:rgb(105, 80, 117)\\n}")
        self.verticalLayout = QVBoxLayout(self.cond_range_groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.highcondlabel = QLabel(self.cond_range_groupBox)
        self.highcondlabel.setObjectName(u"highcondlabel")

        self.horizontalLayout_8.addWidget(self.highcondlabel)

        self.highcond_lineEdit = QLineEdit(self.cond_range_groupBox)
        self.highcond_lineEdit.setObjectName(u"highcond_lineEdit")
        self.highcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.highcond_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_8.addWidget(self.highcond_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.lowcondlabel = QLabel(self.cond_range_groupBox)
        self.lowcondlabel.setObjectName(u"lowcondlabel")

        self.horizontalLayout_11.addWidget(self.lowcondlabel)

        self.lowcond_lineEdit = QLineEdit(self.cond_range_groupBox)
        self.lowcond_lineEdit.setObjectName(u"lowcond_lineEdit")
        self.lowcond_lineEdit.setMinimumSize(QSize(50, 20))
        self.lowcond_lineEdit.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_11.addWidget(self.lowcond_lineEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_11, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.gridLayout_2.setColumnMinimumWidth(0, 1)
        self.gridLayout_2.setColumnMinimumWidth(2, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout_2.addWidget(self.cond_range_groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.square_label_7.setText(QCoreApplication.translate("Form", u"New Method", None))
        self.peaknumlabel.setText(QCoreApplication.translate("Form", u"Peak Num", None))
        self.peaknum_lineEdit.setText(QCoreApplication.translate("Form", u"0", None))
        self.amplitudelabel.setText(QCoreApplication.translate("Form", u"Hover Amplitude", None))
        self.hoveramplitude_lineEdit.setText(QCoreApplication.translate("Form", u"1", None))
        self.interceplabel.setText(QCoreApplication.translate("Form", u"Threshold", None))
        self.threshold_lineEdit.setText(QCoreApplication.translate("Form", u"0.1", None))
        self.sine1dlabel.setText(QCoreApplication.translate("Form", u"1D_Fit_Length", None))
        self.length1dfit_lineEdit.setText(QCoreApplication.translate("Form", u"0", None))
        self.range_open_checkBox.setText(QCoreApplication.translate("Form", u"Open", None))
        self.cond_range_groupBox.setTitle(QCoreApplication.translate("Form", u"Conduction Range", None))
        self.highcondlabel.setText(QCoreApplication.translate("Form", u"HIGH COND", None))
        self.highcond_lineEdit.setText(QCoreApplication.translate("Form", u"-1", None))
        self.lowcondlabel.setText(QCoreApplication.translate("Form", u"LOW COND", None))
        self.lowcond_lineEdit.setText(QCoreApplication.translate("Form", u"-5", None))
    # retranslateUi

