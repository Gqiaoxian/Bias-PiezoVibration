# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pcabutton.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QToolButton,
    QWidget)
import ui.images_rc

class Ui_pcabutton(object):
    def setupUi(self, pcabutton):
        if not pcabutton.objectName():
            pcabutton.setObjectName(u"pcabutton")
        pcabutton.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(pcabutton)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.open_pushButton = QToolButton(pcabutton)
        self.open_pushButton.setObjectName(u"open_pushButton")
        self.open_pushButton.setMinimumSize(QSize(60, 40))
        self.open_pushButton.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        self.open_pushButton.setFont(font)
        icon = QIcon()
        icon.addFile(u":/png/images/openfile.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_pushButton.setIcon(icon)
        self.open_pushButton.setIconSize(QSize(20, 20))
        self.open_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.open_pushButton)

        self.run_pushButton = QToolButton(pcabutton)
        self.run_pushButton.setObjectName(u"run_pushButton")
        self.run_pushButton.setMinimumSize(QSize(60, 40))
        self.run_pushButton.setMaximumSize(QSize(60, 16777215))
        self.run_pushButton.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/png/images/run.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run_pushButton.setIcon(icon1)
        self.run_pushButton.setIconSize(QSize(20, 20))
        self.run_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.run_pushButton)

        self.save_pushButton = QToolButton(pcabutton)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setMinimumSize(QSize(60, 40))
        self.save_pushButton.setMaximumSize(QSize(60, 16777215))
        self.save_pushButton.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u":/png/images/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_pushButton.setIcon(icon2)
        self.save_pushButton.setIconSize(QSize(20, 20))
        self.save_pushButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.horizontalLayout.addWidget(self.save_pushButton)


        self.retranslateUi(pcabutton)

        QMetaObject.connectSlotsByName(pcabutton)
    # setupUi

    def retranslateUi(self, pcabutton):
        pcabutton.setWindowTitle(QCoreApplication.translate("pcabutton", u"Form", None))
        self.open_pushButton.setText(QCoreApplication.translate("pcabutton", u"Open", None))
        self.run_pushButton.setText(QCoreApplication.translate("pcabutton", u"Run", None))
        self.save_pushButton.setText(QCoreApplication.translate("pcabutton", u"Save", None))
    # retranslateUi

