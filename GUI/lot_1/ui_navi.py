# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'naviYlGdre.ui'
##
## Created by: Qt User Interface Compiler version 5.15.13
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1437, 716)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_label = QLabel(self.centralwidget)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(0, 0, 1440, 718))
        self.main_label.setStyleSheet(u"background-color : rgb(222, 255, 248)")
        self.main_label.setPixmap(QPixmap(u":/parkinglot/prototype.jpg"))
        self.main_label.setScaledContents(True)
        self.main_label.setWordWrap(False)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.main_label.setText("")
    # retranslateUi

