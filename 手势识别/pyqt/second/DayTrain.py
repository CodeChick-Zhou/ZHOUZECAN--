from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from NN_multiplication_table import NN_Table
from Random_practice import Random_Practice
import time


# 等待短暂时间使得其他定时器可以退出
class SleepThread(QThread):
    def __init__(self):
        super().__init__()


    timer = pyqtSignal()
    def run(self):
        time.sleep(0.8)
        self.timer.emit()


class DayTrain(object):
    def __init__(self,parents):
        super().__init__()
        # 为了获得坐标，传入父对象
        self.curparents = parents

        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(1200, 900)

        self.initThread()
        self.init_frame(parents)


    def initThread(self):
        self.Sleepthread = SleepThread()
        self.Sleepthread.timer.connect(self.ButtonConnect)

    def init_frame(self,parents):
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 200, 300, 680))
        self.verticalLayoutWidget.setObjectName("ButtonWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("ButtonLayout")

        self.pushButton_1 = QtWidgets.QPushButton("九九乘法表", self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("HomeButton")
        self.pushButton_1.setIcon(QIcon("../images/考试.png"))
        self.pushButton_1.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_1)
        self.pushButton_1.clicked.connect(self.ShowNNTable)

        self.pushButton_2 = QtWidgets.QPushButton("随即练习", self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("HomeButton")
        self.pushButton_2.setIcon(QIcon("../images/考试.png"))
        self.pushButton_2.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.ShowRandomPe)

        self.pushButton_3 = QtWidgets.QPushButton("设置", self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("HomeButton")
        self.pushButton_3.setIcon(QIcon("../images/考试.png"))
        self.pushButton_3.setFixedSize(300, 40)
        self.pushButton_3.clicked.connect(self.ShowDialog)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton("回主菜单", self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("HomeButton")
        self.pushButton_4.setIcon(QIcon("../images/考试.png"))
        self.pushButton_4.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_4)

        # self.pushButton_3.clicked.connect(self.ShowDialog)

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
            QPushButton{border:none;color:white;font-size:25px}
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

        self.Widget1 = NN_Table(self.curparents)
        self.Widget1.frame.setVisible(False)

        self.Widget2 = Random_Practice(self.curparents)
        self.Widget2.frame.setVisible(False)


        self.Widget1.right_button_2.clicked.connect(self.on_pushButton_enter_clicked_sleep1)
        self.Widget2.right_button_2.clicked.connect(self.on_pushButton_enter_clicked_sleep2)


    def ShowNNTable(self):
        self.Widget1.frame.setVisible(True)
        self.frame.setVisible(False)
        self.Widget1.Start(self.Timing)

    def ShowRandomPe(self):
        self.Widget2.frame.setVisible(True)
        self.frame.setVisible(False)
        self.Widget2.Start(self.Timing)


    def on_pushButton_enter_clicked_sleep1(self):
        self.Widget1.right_button_1.setEnabled(False)
        self.Widget1.right_button_2.setEnabled(False)
        self.Widget1.right_button_3.setEnabled(False)
        self.Sleepthread.start()

    def on_pushButton_enter_clicked_sleep2(self):
        self.Widget2.right_button_1.setEnabled(False)
        self.Widget2.right_button_2.setEnabled(False)
        self.Widget2.right_button_3.setEnabled(False)
        self.Sleepthread.start()

    def ButtonConnect(self):
        self.on_pushButton_enter_clicked()
        self.Widget1.right_button_1.setEnabled(True)
        self.Widget1.right_button_2.setEnabled(True)
        self.Widget1.right_button_3.setEnabled(True)
        self.Widget2.right_button_1.setEnabled(True)
        self.Widget2.right_button_2.setEnabled(True)
        self.Widget2.right_button_3.setEnabled(True)

    def on_pushButton_enter_clicked(self):
        self.Widget1.frame.setVisible(False)
        self.Widget2.frame.setVisible(False)
        # self.Widget3.frame1.setVisible(False)
        self.frame.setVisible(True)

    # 显示设置对话框
    def ShowDialog(self):
        self.Exdialog = QDialog()

        self.Exdialog.resize(420, 200)
        self.Exdialog.setFixedSize(420, 200)

        self.ExdialogWidget = QWidget(self.Exdialog)
        self.ExdialogWidget.resize(420, 200)
        self.ExdialogWidget.setFixedSize(420, 200)
        self.ExdialogWidget.setObjectName("dialog")

        self.label1 = QLabel(self.ExdialogWidget)
        self.label1.setText("时间设置")
        self.label1.setObjectName('label1')
        self.label1.setGeometry(QtCore.QRect(20, 40, 100, 80))
        self.ExdialogWidget.setStyleSheet("QLabel#label1{font-size:20px}")

        self.label1_button_left = QPushButton(self.ExdialogWidget)
        self.label1_button_right = QPushButton(self.ExdialogWidget)
        self.label1_button_left.setObjectName('btn1')
        self.label1_button_right.setObjectName('btn2')

        self.label1_button_left.setGeometry(QtCore.QRect(130, 50, 50, 50))
        self.label1_button_right.setGeometry(QtCore.QRect(300, 50, 50, 50))
        self.label1_button_left.clicked.connect(self.time_reduce)
        self.label1_button_right.clicked.connect(self.time_add)


        self.label1_LineEdit = QLineEdit(self.ExdialogWidget)
        self.label1_LineEdit.setGeometry(QtCore.QRect(190, 60, 100, 40))
        self.label1_LineEdit.setText(str(self.Timing))
        self.label1_LineEdit.setAlignment(Qt.AlignCenter)
        self.label1_LineEdit.setReadOnly(True)


        self.sbutton = QPushButton(self.ExdialogWidget)
        self.sbutton.setText("确定")
        self.sbutton.clicked.connect(self.Exdialog.close)
        self.sbutton.setGeometry(QtCore.QRect(280, 140, 100, 40))
        self.sbutton.setStyleSheet('''
            QPushButton{
                background:#a1f8ba;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QPushButton:hover{font-size:18px;background:#a1f8ba}
        ''')

        # self.Exdialog.setObjectName("ExDialog")

        self.Exdialog.setWindowTitle('选择难度')
        self.Exdialog.setWindowModality(Qt.ApplicationModal)

        self.Exdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.Exdialog.setWindowOpacity(1)  # 设置窗口透明度
        self.Exdialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # EAE5C9  6CC6CB

        self.Exdialog.setStyleSheet('''
        QWidget#dialog{
                background:QLinearGradient(x1:1, y1:1, x2:0, y2:0, stop:0 #EEEECE, stop:1 #6CC6CB);
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                }
        QLineEdit{
                background: rgb(230,230,230);
                border-radius: 8px;
                border:1px solid rgb(180, 180, 180);
                font-size:25px}

        QPushButton#btn1{border-image: url(./images/左箭头.png)}
        QPushButton#btn1:hover{border-image: url(./images/左箭头选中.png)}
        QPushButton#btn2{border-image: url(./images/右箭头.png)}
        QPushButton#btn2:hover{border-image: url(./images/右箭头选中.png)}
        ''')

        size1 = self.frame.geometry()
        size2 = self.Exdialog.geometry()
        self.Exdialog.move( self.curparents.x()+(size1.width()-size2.width())/2,
                            self.curparents.y()+(size1.height()-size2.height())/2)

        self.Exdialog.exec()

    Timing = 10
    # 减少时间
    def time_reduce(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 3:
            return
        else:
            self.Timing -= 1
            self.label1_LineEdit.setText(str(self.Timing))

    # 增加时间
    def time_add(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 30:
            return
        else:
            self.Timing += 1
            self.label1_LineEdit.setText(str(self.Timing))
        return

