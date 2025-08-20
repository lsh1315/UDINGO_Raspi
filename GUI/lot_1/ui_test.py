# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testDvvWSL.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setMinimumSize(QSize(1280, 800))
        MainWindow.setAnimated(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1280, 800))
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(1280, 800))
        self.stackedWidget.setStyleSheet(u"")
        self.preference1 = QWidget()
        self.preference1.setObjectName(u"preference1")
        self.background1 = QLabel(self.preference1)
        self.background1.setObjectName(u"background1")
        self.background1.setGeometry(QRect(0, 0, 1280, 800))
        self.background1.setMinimumSize(QSize(1280, 800))
        self.background1.setPixmap(QPixmap(u":/preference/001.png"))
        self.elec = QPushButton(self.preference1)
        self.elec.setObjectName(u"elec")
        self.elec.setGeometry(QRect(210, 300, 151, 151))
        self.elec.setStyleSheet(u"background-color:rgb(214, 226, 232);")
        icon = QIcon()
        icon.addFile(u":/button/KakaoTalk_20250820_112752795.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.elec.setIcon(icon)
        self.elec.setIconSize(QSize(150, 150))
        self.big = QPushButton(self.preference1)
        self.big.setObjectName(u"big")
        self.big.setGeometry(QRect(390, 300, 151, 151))
        self.big.setStyleSheet(u"background-color:rgb(214, 226, 232);")
        icon1 = QIcon()
        icon1.addFile(u":/button/KakaoTalk_20250820_112752795_02.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.big.setIcon(icon1)
        self.big.setIconSize(QSize(150, 150))
        self.handicap = QPushButton(self.preference1)
        self.handicap.setObjectName(u"handicap")
        self.handicap.setGeometry(QRect(210, 490, 151, 151))
        self.handicap.setStyleSheet(u"background-color:rgb(214, 226, 232);")
        icon2 = QIcon()
        icon2.addFile(u":/button/KakaoTalk_20250820_112752795_03.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.handicap.setIcon(icon2)
        self.handicap.setIconSize(QSize(150, 150))
        self.small = QPushButton(self.preference1)
        self.small.setObjectName(u"small")
        self.small.setGeometry(QRect(390, 490, 151, 151))
        self.small.setStyleSheet(u"background-color:rgb(214, 226, 232);")
        icon3 = QIcon()
        icon3.addFile(u":/button/KakaoTalk_20250820_112752795_01.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.small.setIcon(icon3)
        self.small.setIconSize(QSize(150, 150))
        self.stackedWidget.addWidget(self.preference1)
        self.preference2 = QWidget()
        self.preference2.setObjectName(u"preference2")
        self.background2 = QLabel(self.preference2)
        self.background2.setObjectName(u"background2")
        self.background2.setGeometry(QRect(0, 0, 1280, 800))
        self.background2.setMinimumSize(QSize(1280, 800))
        self.background2.setPixmap(QPixmap(u":/preference/002.png"))
        self.Entrance = QPushButton(self.preference2)
        self.Entrance.setObjectName(u"Entrance")
        self.Entrance.setGeometry(QRect(200, 290, 391, 101))
        font = QFont()
        font.setPointSize(36)
        self.Entrance.setFont(font)
        self.Entrance.setStyleSheet(u"background-color: rgb(112, 177, 186);")
        self.Exit = QPushButton(self.preference2)
        self.Exit.setObjectName(u"Exit")
        self.Exit.setGeometry(QRect(200, 410, 391, 101))
        self.Exit.setFont(font)
        self.Exit.setStyleSheet(u"background-color: rgb(112, 177, 186);")
        self.Mall = QPushButton(self.preference2)
        self.Mall.setObjectName(u"Mall")
        self.Mall.setGeometry(QRect(200, 530, 391, 101))
        self.Mall.setFont(font)
        self.Mall.setStyleSheet(u"background-color: rgb(112, 177, 186);")
        self.stackedWidget.addWidget(self.preference2)
        self.navi = QWidget()
        self.navi.setObjectName(u"navi")
        self.navi.setMinimumSize(QSize(1280, 800))
        self.navi.setStyleSheet(u"")
        self.car = QLabel(self.navi)
        self.car.setObjectName(u"car")
        self.car.setGeometry(QRect(200, 540, 151, 131))
        self.car.setPixmap(QPixmap(u":/car/free-icon-car-1047003.png"))
        self.car.setScaledContents(True)
        self.map = QLabel(self.navi)
        self.map.setObjectName(u"map")
        self.map.setGeometry(QRect(0, 0, 1280, 800))
        self.map.setMinimumSize(QSize(1280, 800))
        self.map.setPixmap(QPixmap(u":/parkinglot/003.png"))
        self.map.setScaledContents(False)
        self.terminate = QPushButton(self.navi)
        self.terminate.setObjectName(u"terminate")
        self.terminate.setGeometry(QRect(1190, 740, 75, 41))
        font1 = QFont()
        font1.setFamilies([u"\ud734\uba3c\ubaa8\uc74cT"])
        font1.setPointSize(10)
        self.terminate.setFont(font1)
        self.terminate.setStyleSheet(u"background-color:rgb(211, 0, 0);")
        self.stackedWidget.addWidget(self.navi)
        self.map.raise_()
        self.car.raise_()
        self.terminate.raise_()

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.big.clicked.connect(MainWindow.save_type)
        self.Entrance.clicked.connect(MainWindow.save_near)
        self.terminate.clicked.connect(MainWindow.terminate)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.background1.setText("")
        self.elec.setText("")
        self.big.setText("")
        self.handicap.setText("")
        self.small.setText("")
        self.background2.setText("")
        self.Entrance.setText(QCoreApplication.translate("MainWindow", u"Entrance", None))
        self.Exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.Mall.setText(QCoreApplication.translate("MainWindow", u"Mall", None))
        self.car.setText("")
        self.map.setText("")
        self.terminate.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc", None))
    # retranslateUi

