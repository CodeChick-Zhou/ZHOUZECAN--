from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import copy
import random
from finger_train import *
import picture as pic
import cv2
import sys
import qtawesome
from VideoWorkThread import VideoSingleton




class Examination(object):
    def __init__(self,parents):
        super().__init__()
        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(1200, 900)

        self.ButtonFlag = True
        self.init_fram(parents)

        self.frame1 = QWidget(parents)
        self.frame1.setObjectName("Frame1")
        self.frame1.resize(1200, 900)
        self.frame1.setFixedSize(1200, 900)
        # self.init_fram1(parents)
        #
        self.pushButtondd = QtWidgets.QPushButton("10道题考试", self.frame1)

    def showDialog(self):
        self.Exdialog = QDialog()

        self.Exdialog.resize(300,100)
        self.Exdialog.setFixedSize(300,100)

        self.HLayout = QtWidgets.QWidget(self.Exdialog)
        # self.HLayout.setGeometry(QtCore.QRect(0, 0, 300, 50))
        self.button1 = QPushButton('容易',self.HLayout)
        self.button1.setObjectName("DialogButton")
        self.button2 = QPushButton('中等', self.HLayout)
        self.button2.setObjectName("DialogButton")
        self.button3 = QPushButton('设置困难', self.HLayout)
        self.button3.setObjectName("DialogButton")

        self.button1.clicked.connect(self.Exdialog.close)
        self.button1.clicked.connect(lambda :self.SetDifficulty(0))
        self.button2.clicked.connect(self.Exdialog.close)
        self.button2.clicked.connect(lambda: self.SetDifficulty(1))
        self.button3.clicked.connect(self.Exdialog.close)
        self.button3.clicked.connect(lambda: self.SetDifficulty(2))

        self.Exdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.Exdialog.setWindowOpacity(1)  # 设置窗口透明度
        # self.Exdialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.button1.setFixedSize(100,50)
        self.button2.setFixedSize(100,50)
        self.button3.setFixedSize(100,50)

        self.button1.move(0,30)
        self.button2.move(100, 30)
        self.button3.move(200, 30)

        self.Exdialog.setObjectName("ExDialog")


        self.Exdialog.setStyleSheet('''
        QDialog{
                background:QLinearGradient(x1:1, y1:1, x2:0, y2:0, stop:0 rgb(211,149,155), stop:1 rgb(191,230,186));
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                }
        ''')
        self.HLayout.setStyleSheet('''
            QPushButton{border:none;color:white;font-size:20px}
            QPushButton:hover{
                    border-left:4px solid white;
                    font-size:23px;
                    background:#4affa5;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
        ''')

        self.Exdialog.setWindowTitle('选择难度')
        self.Exdialog.setWindowModality(Qt.ApplicationModal)

        self.Exdialog.exec()


    def exam(self):
        self.frame.setVisible(False)
        self.frame1.setVisible(True)

    # 0-Easy 1-Medium 2-difficult
    Difficulty = 0
    # Easy-180  Medium-120   difficult-180
    Timing = 180
    # Number of questions
    NumberQuestions = 10
    def SetDifficulty(self,result):
        self.Difficulty = result
        print("Difficulty :",self.Difficulty)
        if self.Difficulty == 0 :
            self.Timing = 180
        elif self.Difficulty == 1:
            self.Timing = 120
        elif self.Difficulty == 2:
            self.Timing = 60

    def init_fram1(self,parents):
        self.horizontalLayoutWidget1 = QtWidgets.QWidget(self.frame1)
        self.horizontalLayoutWidget1.setGeometry(QtCore.QRect(1000, 0, 200, 111))
        self.horizontalLayoutWidget1.setObjectName("TopButtonWidget")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget1)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setObjectName("TopButtonLayout")
        self.pushButton_min1 = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.pushButton_min1.setObjectName("HomeTopButton")
        self.horizontalLayout1.addWidget(self.pushButton_min1)
        self.pushButton_close1 = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.pushButton_close1.setObjectName("HomeTopButton")
        self.horizontalLayout1.addWidget(self.pushButton_close1)
        self.pushButton_min1.setFixedSize(25, 25)  # 设置关闭按钮的大小
        self.pushButton_close1.setFixedSize(25, 25)  # 设置最小化按钮大小
        self.pushButton_min1.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_close1.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.pushButton_min1.clicked.connect(parents.showMinimized)
        self.pushButton_close1.clicked.connect(parents.close)

        self.verticalLayoutWidget1 = QtWidgets.QWidget(self.frame1)
        self.verticalLayoutWidget1.setGeometry(QtCore.QRect(450, 200, 300, 600))
        self.verticalLayoutWidget1.setObjectName("ButtonWidget")
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget1)

        self.verticalLayout1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout1.setObjectName("ButtonLayout")

        self.pushButton_11 = QtWidgets.QPushButton("10道题考试", self.verticalLayoutWidget1)
        self.pushButton_11.setObjectName("HomeButton")
        self.pushButton_11.setIcon(QIcon("../images/考试.png"))
        self.pushButton_11.setFixedSize(300, 40)
        self.verticalLayout1.addWidget(self.pushButton_11)
        self.pushButton_11.clicked.connect(self.exam)

        self.pushButton_21 = QtWidgets.QPushButton("20道题考试", self.verticalLayoutWidget1)
        self.pushButton_21.setObjectName("HomeButton")
        self.pushButton_21.setIcon(QIcon("../images/考试.png"))
        self.pushButton_21.setFixedSize(300, 40)
        self.verticalLayout1.addWidget(self.pushButton_21)

        self.pushButton_31 = QtWidgets.QPushButton("设置", self.verticalLayoutWidget1)
        self.pushButton_31.setObjectName("HomeButton")
        self.pushButton_31.setIcon(QIcon("../images/考试.png"))
        self.pushButton_31.setFixedSize(300, 40)
        self.verticalLayout1.addWidget(self.pushButton_31)

        self.pushButton_41 = QtWidgets.QPushButton("回主菜单", self.verticalLayoutWidget1)
        self.pushButton_41.setObjectName("HomeButton")
        self.pushButton_41.setIcon(QIcon("../images/考试.png"))
        self.pushButton_41.setFixedSize(300, 40)
        self.verticalLayout1.addWidget(self.pushButton_41)

        self.pushButton_31.clicked.connect(self.showDialog)

        # self.pushButton_4.clicked.connect(self.close)

        self.frame1.setStyleSheet('''
                    QWidget#Frame{
                        border-image:url(../images/screen4.jpg);
                        border-top:1px solid white;
                        border-bottom:1px solid white;
                        border-right:1px solid white;
                        border-top-left-radius:10px;
                        border-bottom-left-radius:10px;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                ''')
        self.verticalLayoutWidget1.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:20px}
                            QPushButton:hover{
                                border-left:4px solid white;
                                font-size:23px;
                                background:#4affa5;
                                border-top:1px solid white;
                                border-bottom:1px solid white;
                                border-left:1px solid white;
                                border-top-left-radius:10px;
                                border-bottom-left-radius:10px;
                                border-top-right-radius:10px;
                                border-bottom-right-radius:10px;
                                }
                        ''')

    def init_fram(self,parents):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(1000, 0, 200, 111))
        self.horizontalLayoutWidget.setObjectName("TopButtonWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("TopButtonLayout")
        self.pushButton_min = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_min.setObjectName("HomeTopButton")
        self.horizontalLayout.addWidget(self.pushButton_min)
        self.pushButton_close = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_close.setObjectName("HomeTopButton")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.pushButton_min.setFixedSize(25, 25)  # 设置关闭按钮的大小
        self.pushButton_close.setFixedSize(25, 25)  # 设置最小化按钮大小
        self.pushButton_min.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.pushButton_min.clicked.connect(parents.showMinimized)
        self.pushButton_close.clicked.connect(parents.close)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 200, 300, 600))
        self.verticalLayoutWidget.setObjectName("ButtonWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("ButtonLayout")

        self.pushButton_1 = QtWidgets.QPushButton("10道题考试", self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("HomeButton")
        self.pushButton_1.setIcon(QIcon("../images/考试.png"))
        self.pushButton_1.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_1)
        self.pushButton_1.clicked.connect(self.exam)


        self.pushButton_2 = QtWidgets.QPushButton("20道题考试", self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("HomeButton")
        self.pushButton_2.setIcon(QIcon("../images/考试.png"))
        self.pushButton_2.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton("设置", self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("HomeButton")
        self.pushButton_3.setIcon(QIcon("../images/考试.png"))
        self.pushButton_3.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton("回主菜单", self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("HomeButton")
        self.pushButton_4.setIcon(QIcon("../images/考试.png"))
        self.pushButton_4.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_3.clicked.connect(self.showDialog)

        # self.pushButton_4.clicked.connect(self.close)

        self.frame.setStyleSheet('''
            QWidget#Frame{
                border-image:url(../images/screen4.jpg);
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-right:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')
        self.verticalLayoutWidget.setStyleSheet('''
                    QPushButton{border:none;color:white;font-size:20px}
                    QPushButton:hover{
                        border-left:4px solid white;
                        font-size:23px;
                        background:#4affa5;
                        border-top:1px solid white;
                        border-bottom:1px solid white;
                        border-left:1px solid white;
                        border-top-left-radius:10px;
                        border-bottom-left-radius:10px;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                        }
                ''')
