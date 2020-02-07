from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import random
import sys
import qtawesome

NumberDict = {'1': "../images/number1.png", '2': "../images/number2.png", '3': "../images/number3.png",
              '4': "../images/number4.png", '5': "../images/number5.png", '6': "../images/number6.png",
              '7': "../images/number7.png", '8': "../images/number8.png", '9': "../images/number1.png",
              '0': "../images/number0.png"}

SymbolDict = {0: "../images/加号.png", 1: "../images/减号.png" , 2: "../images/乘号.png"}

# 九九乘法表
Multiplication_Table = {0 : 1, 1 : 2,  2 : 3,  3 : 4,   4 : 5,   5 : 6,   6 : 7,   7 : 8,   8 : 9,
                        9 : 4, 10 : 6, 11 : 8, 12 : 10, 13 : 12, 14 : 14, 15 : 16, 16 : 18,
                        17 : 9, 18 : 12, 19 : 15, 20 : 18, 21 : 21, 22 : 24, 23 : 27,
                        24 : 16, 25 : 20, 26 : 24, 27 : 28, 28 : 32, 29 : 36,
                        30 : 25, 31 : 30, 32 : 35, 33 : 40, 34 : 45,
                        35 : 36, 36 : 42, 37 : 48, 38 : 54,
                        39 : 49, 40 : 56, 41 : 63,
                        42 : 64, 43 : 72,
                        44 : 81
                        }

Qmut = QMutex()
StopFlag = False
sec = 30
class TimeWorkThread(QThread):

    def __init__(self):
        super().__init__()

    timer = pyqtSignal()   # 每隔1秒发送一次信号
    end = pyqtSignal()     # 计数完成后发送一次信号
    def run(self):
        Qmut.lock()        # 加锁防止出现两个线程
        global sec
        while True:
            if StopFlag:
                break

            self.sleep(1)  # 休眠1秒
            if sec == 0:
                self.end.emit()   # 发送end信号
                break
            self.timer.emit()   # 发送timer信号
        Qmut.unlock()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class NN_Table(object):
    def __init__(self,parents):
        super().__init__()
        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(1200, 900)

        self.ButtonFlag = True
        self.init_fram()

    # 计数器
    def countTime(self):
        global sec

        sec -= 1
        if sec < 0:
            return
        elif sec <= 9:
            self.ChangeNumberTime(self.right_top_label_1,self.right_top_label_2,0,sec)
        elif sec > 9:
            a = int(sec/10)
            print(a)
            b = sec%10
            self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, a, b)


    def end(self):
        self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
        self.right_bottom_label_1.setScaledContents(True)
        self.right_button_1.setText("下一题")
        self.ButtonFlag = False

    def NN_Start(self):
        global StopFlag
        global sec

        sec = 30
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec/10), int(sec%10))

        StopFlag = False
        self.value1 = -1
        self.value2 = -1
        self.value3 = -1
        self.value4 = -1

        index = random.randint(0, 44)
        self.value = Multiplication_Table[index]
        self.value3 = int(self.value/10)
        self.value4 = int(self.value%10)

        if self.value3 == 0:
            self.right_Number_LineEdit_4.setHidden(True)
            self.ChangeNumberImage(self.right_Number_LineEdit_3, self.value4)
        else:
            self.right_Number_LineEdit_4.setHidden(False)
            self.ChangeNumberImage(self.right_Number_LineEdit_3, self.value3)
            self.ChangeNumberImage(self.right_Number_LineEdit_4, self.value4)

        self.ChangeNumberImage(self.right_Number_LineEdit_1, -1)
        self.ChangeNumberImage(self.right_Number_LineEdit_2, -1)

        self.NN_Table_Start()

    def NN_Table_Start(self):
        self.timerthread = TimeWorkThread()
        self.timerthread.timer.connect(self.countTime)
        self.timerthread.end.connect(self.end)
        self.timerthread.start()


    def textchanged(self,right_Number_LineEdit,number):
        text = right_Number_LineEdit.text()
        if text == "":
            return

        if not is_number(text):
            right_Number_LineEdit.setText("")
            return

        if number == 1:
            self.value1 = int(text)
        elif number == 2:
            self.value2 = int(text)

        if int(text)>=0 & int(text)<=9:
            self.ChangeNumberImage(right_Number_LineEdit,int(text))


        print("before right_Number_LineEdit_1 text:",self.right_Number_LineEdit_1.text())
        right_Number_LineEdit.setText("")
        print("after right_Number_LineEdit_1 text:", self.right_Number_LineEdit_1.text())

    # 线程中改变数值
    def ChangeNumberTime(self,label1,label2,a,b):
        label1.setPixmap(QPixmap("../images/number"+str(a)+".png"))
        label1.setScaledContents(True)  # 让图片自适应label大小
        label2.setPixmap(QPixmap("../images/number"+str(b)+".png"))
        label2.setScaledContents(True)  # 让图片自适应label大小

    # 改变编辑框的图片
    def ChangeNumberImage(self,right_Number_LineEdit,number):
        if number == -1:
            filename = "../images/空.png"
        else:
            filename = "../images/number"+str(number)+".png"
        print("filename:",filename)
        pal = right_Number_LineEdit.palette()
        pal.setBrush(QPalette.Base,QBrush(QPixmap(filename).scaled(right_Number_LineEdit.size())))
        right_Number_LineEdit.setAutoFillBackground(True)
        right_Number_LineEdit.setPalette(pal)

    def init_fram(self):
        self.right_Number_LineEdit_1 = QLineEdit(self.frame)
        self.right_Number_LineEdit_1.setObjectName('right_Number')
        self.right_Number_LineEdit_2 = QLineEdit(self.frame)
        self.right_Number_LineEdit_2.setObjectName('right_Number')
        self.right_Number_LineEdit_3 = QLineEdit(self.frame)
        self.right_Number_LineEdit_3.setObjectName('right_Number')
        self.right_Number_LineEdit_4 = QLineEdit(self.frame)
        self.right_Number_LineEdit_4.setObjectName('right_Number')
        self.right_label1 = QLabel(self.frame)
        self.right_label2 = QLabel(self.frame)

        self.right_Number_LineEdit_1.setGeometry(QtCore.QRect(110, 400, 140, 200))
        self.right_label1.setGeometry(QtCore.QRect(260, 450, 140, 100))
        self.right_Number_LineEdit_2.setGeometry(QtCore.QRect(410, 400, 140, 200))
        self.right_label2.setGeometry(QtCore.QRect(550, 450, 140, 100))
        self.right_Number_LineEdit_3.setGeometry(QtCore.QRect(710, 400, 140, 200))
        self.right_Number_LineEdit_4.setGeometry(QtCore.QRect(850, 400, 140, 200))

        self.right_Number_LineEdit_1.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_2.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_3.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_4.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_1.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_1,1))
        self.right_Number_LineEdit_2.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_2,2))
        self.right_Number_LineEdit_3.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_3,3))
        self.right_Number_LineEdit_4.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_4,4))

        self.right_Number_LineEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.right_Number_LineEdit_4.setFocusPolicy(QtCore.Qt.NoFocus)

        self.right_button_2 = QtWidgets.QPushButton("退出", self.frame)
        self.right_button_2.clicked.connect(self.DeleteFram)
        self.right_top_time_label = QLabel(self.frame)
        self.right_top_label_1 = QLabel(self.frame)
        self.right_top_label_2 = QLabel(self.frame)
        self.right_bottom_label_1 = QLabel(self.frame)

        self.right_button_2.setGeometry(QtCore.QRect(1050, 0, 100, 50))
        self.right_button_2.setStyleSheet('''
            QPushButton{
                    background:#ff3c3c;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
            QPushButton:hover{font-size:18px;background:red}
            ''')
        self.right_top_time_label.setGeometry(QtCore.QRect(500, 0, 130, 140))
        self.right_top_label_1.setGeometry(QtCore.QRect(480, 140, 80, 120))
        self.right_top_label_2.setGeometry(QtCore.QRect(550, 140, 80, 120))
        self.right_bottom_label_1.setGeometry(QtCore.QRect(490, 720, 200, 140))
        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(../images/number2.png")
        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(:../images/number2.png);\n""background-attachment:fixed;\n""background-repeat:none;\n""background-position:center")

        self.right_top_time_label.setPixmap(QPixmap("../images/time.png"))
        self.right_top_time_label.setScaledContents(True)  # 让图片自适应label大小


        self.right_top_label_1.setPixmap(QPixmap("../images/number3.png"))
        self.right_top_label_1.setScaledContents(True)  # 让图片自适应label大小

        self.right_top_label_2.setPixmap(QPixmap("../images/number0.png"))
        self.right_top_label_2.setScaledContents(True)  # 让图片自适应label大小

        self.right_label1.setToolTip('这是一个乘号标签')
        self.right_label1.setPixmap(QPixmap("../images/乘号.png"))
        self.right_label1.setScaledContents(True)  # 让图片自适应label大小

        self.right_label2.setToolTip('这是一个等号标签')
        self.right_label2.setPixmap(QPixmap("../images/等号.png"))
        self.right_label2.setScaledContents(True)  # 让图片自适应label大小2

        self.right_button_1 = QtWidgets.QPushButton("确定", self.frame)
        self.right_button_1.setGeometry(QtCore.QRect(1050, 830, 100, 50))
        self.right_button_1.clicked.connect(self.ChangeButtonStatus)
        self.right_button_1.setStyleSheet('''
            QPushButton{
                    background:#7bffbd;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
            QPushButton:hover{font-size:18px;background:#4affa5}
            ''')

        # background:QLinearGradient(x1:1, y1:1, x2:0, y2:0, stop:0 rgb(211,149,155), stop:1 rgb(191,230,186));
        # border-image: url(:../ images / screen2.jpg);
        self.frame.setStyleSheet('''
            QWidget#Frame{
                border-image:url(../images/screen2.jpg);
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-right:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')

    # 判断公式两边是否正确
    def IsTrue(self):
        Avalue = self.value1 * self.value2
        if Avalue == self.value:
            return True
        else:
            return False

    # 确定和下一题按钮触发的事件
    def ChangeButtonStatus(self):
        if self.ButtonFlag == True:
            if self.IsTrue():
                self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            else:
                self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

            global StopFlag
            StopFlag = True

            self.right_button_1.setText("下一题")
            self.ButtonFlag = False
        else:
            self.NN_Start()
            self.right_bottom_label_1.setPixmap(QPixmap("../images/空号.png"))
            self.right_button_1.setText("确定")
            self.ButtonFlag = True

    def DeleteFram(self):
        global StopFlag
        global sec
        self.ButtonFlag = True
        StopFlag = True
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空号.png"))
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec/10), int(sec%10))

