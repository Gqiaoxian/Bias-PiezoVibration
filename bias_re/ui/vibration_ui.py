# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vibration.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QSizePolicy,
    QVBoxLayout, QWidget)
import ui.images_rc

class Ui_Vibratewidget(object):
    def setupUi(self, Vibratewidget):
        if not Vibratewidget.objectName():
            Vibratewidget.setObjectName(u"Vibratewidget")
        Vibratewidget.resize(610, 536)
        self.verticalLayout_2 = QVBoxLayout(Vibratewidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.plotgroupBox = QGroupBox(Vibratewidget)
        self.plotgroupBox.setObjectName(u"plotgroupBox")
        self.plotgroupBox.setMinimumSize(QSize(0, 300))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.plotgroupBox.setFont(font)
        self.horizontalLayout_3 = QHBoxLayout(self.plotgroupBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.widget_2d = QWidget(self.plotgroupBox)
        self.widget_2d.setObjectName(u"widget_2d")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.widget_2d.setFont(font1)

        self.horizontalLayout_3.addWidget(self.widget_2d)

        self.widget_1d = QWidget(self.plotgroupBox)
        self.widget_1d.setObjectName(u"widget_1d")

        self.horizontalLayout_3.addWidget(self.widget_1d)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 3)

        self.verticalLayout_2.addWidget(self.plotgroupBox)

        self.verticalLayout_2.setStretch(0, 2)

        self.retranslateUi(Vibratewidget)

        QMetaObject.connectSlotsByName(Vibratewidget)
    # setupUi

    def retranslateUi(self, Vibratewidget):
        Vibratewidget.setWindowTitle(QCoreApplication.translate("Vibratewidget", u"Form", None))
        self.plotgroupBox.setTitle(QCoreApplication.translate("Vibratewidget", u"2D-1D", None))
    # retranslateUi

