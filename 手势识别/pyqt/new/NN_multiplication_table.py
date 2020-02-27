
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

Multiplication_Table_Formula = { 0 : [1,1,1], 1 : [1,2,2], 2 : [1,3,3], 3 : [1,4,4], 4 : [1,5,5], 5 : [1,6,6], 6 : [1,7,7], 7 : [1,8,8], 8 : [1,9,9],
                                 9 : [2,2,4], 10 : [2,3,6], 11 : [2,4,8], 12 : [2,5,10], 13 : [2,6,12], 14 : [2,7,14], 15 : [2,8,16], 16 : [2,9,18],
                                 17 : [3,3,9], 18 : [3,4,12], 19 : [3,5,15], 20 : [3,6,18], 21 : [3,7,21], 22 : [3,8,24], 23 : [3,9,27],
                                 24 : [4,4,16], 25 : [4,5,20], 26 : [4,6,24], 27 : [4,7,28], 28 : [4,8,32], 29 : [4,9,36],
                                 30 : [5,5,25], 31 : [5,6,30], 32 : [5,7,35], 33 : [5,8,40], 34 : [5,9,45],
                                 35 : [6,6,36], 36 : [6,7,42], 37 : [6,8,48], 38 : [6,9,54],
                                 39 : [7,7,49], 40 : [7,8,56], 41 : [7,9,63],
                                 42 : [8,8,64], 43 : [8,9,72],
                                 44 : [9,9,81]
                                 }

Multiplication_Table_Pre = { 1 : [[1,1]], 2 : [[1,2]], 3 : [[1,3]], 4 : [[2,2],[1,4]], 5 : [[1,5]], 6 : [[1,6],[2,3]],
                             7 : [[1,7]], 8 : [[1,8],[2,4]], 9 : [[1,9],[3,3]], 10 : [[2,5]], 12 : [[2,6],[3,4]],
                             14 : [[2,7]], 15 : [[3,5]], 16 : [[4,4],[2,8]], 18 : [[2,9],[3,6]], 20 : [[4,5]],
                             21 : [[3,7]], 24 : [[3,8],[4,6]], 25 : [[5,5]], 27 : [[3,9]], 28 : [[4,7]], 30 : [[5,6]],
                             32 : [[4,8]], 35 : [[5,7]], 36 : [[6,6],[4,9]], 40 : [[5,8]], 42 : [[6,7]], 45 : [[5,9]],
                             48 : [[6,8]], 49 : [[7,7]], 54 : [[6,9]], 56 : [[7,8]], 63 : [[7,9]], 72 : [[8,9]],
                             81 : [[9,9]]
                             }

# 定时器加锁，防止多个线程一起运行
QmutNN = QMutex()

# 按钮和超时加锁
Button_timeout = QMutex()

# 定时器停止标志
StopFlag = False

# 手势识别正常结束标志
VideoThreadEnd = False

# 初始化定时器时间
sec = 30

class TimeWorkThread(QThread):
    def __init__(self):
        super().__init__()

    SignalButton = pyqtSignal()  # 恢复按钮触发函数
    timer = pyqtSignal()   # 每隔1秒发送一次信号
    end = pyqtSignal()     # 计数完成后发送一次信号
    def run(self):
        print("九九乘法表 TimeWorkThread RUN")
        QmutNN.lock()        # 加锁防止出现两个线程
        global sec
        while True:
            # print("***********")
            if StopFlag:
                break

            self.sleep(1)  # 休眠1秒

            if StopFlag:
                break
            if sec == 0:
                self.end.emit()   # 发送end信号
                break
            self.timer.emit()   # 发送timer信号
        self.SignalButton.emit()
        print("九九乘法表 TimeWorkThread END")
        QmutNN.unlock()

# 编辑框个数
QLineEditCount = 0

class TimeVideoThread(QThread):

    def __init__(self):
        super().__init__()

    # 手势识别定时器的结束标志
    VideoStopFlag = False
    SignalButton = QtCore.pyqtSignal()
    workthread = QtCore.pyqtSignal()
    timer = QtCore.pyqtSignal()   # 每隔1秒发送一次信号
    # end = pyqtSignal()     # 计数完成后发送一次信号

    def SetVideoSingleton(self,flag):
        self.VideoStopFlag = flag

    def EndTime(self):
        print("九九乘法表 ********发送信号*********")
        self.workthread.emit()
        # print("********发送信号*********")

    def run(self):
        QmutNN.lock()        # 加锁防止出现两个线程
        print("九九乘法表 TimeVideoThread RUN")
        global sec,VideoThreadEnd,QLineEditCount
        sec = 10
        self.timer.emit()  # 发送timer信号
        while QLineEditCount:
            while True:
                if self.VideoStopFlag:
                    self.SignalButton.emit()
                    print(" 九九乘法表 TimeVideoThread END")
                    QmutNN.unlock()
                    return

                self.sleep(1)  # 休眠1秒

                if self.VideoStopFlag:
                    self.SignalButton.emit()
                    print(" 九九乘法表 TimeVideoThread END")
                    QmutNN.unlock()
                    return

                if sec == 0:
                    self.EndTime()
                    break
                self.timer.emit()   # 发送timer信号

                if self.VideoStopFlag:
                    self.SignalButton.emit()
                    print("九九乘法表 TimeVideoThread END")
                    QmutNN.unlock()
                    return

            # print("TimeVideoThread self.VideoStopFlag ", self.VideoStopFlag)
            # print("TimeVideoThread 结束 ",sec)
            # print("QLineEditCount ", QLineEditCount)
            sec = 10
            QLineEditCount -= 1

        VideoThreadEnd = True
        print("九九乘法表 TimeVideoThread END")
        QmutNN.unlock()

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
            b = sec%10
            self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, a, b)

    # 线程类第一次初始化,防止信号绑定多个槽函数
    FirstConnect = True
    def Start(self):
        if self.FirstConnect:
            self.timevideothread = TimeVideoThread()
            self.timevideothread.timer.connect(self.countTime)
            self.timevideothread.workthread.connect(VideoSingleton.work)
            self.timevideothread.SignalButton.connect(self.VideoButtonConnect)
            # VideoSingleton.timer.connect(self.GetTimeVideoResult)

            self.timerthread = TimeWorkThread()
            self.timerthread.timer.connect(self.countTime)
            self.timerthread.end.connect(self.end)
            self.timerthread.SignalButton.connect(self.ButtonConnect)

            self.FirstConnect = False

        print("VideoSingleton.timer.disconnect()")
        VideoSingleton.timer.connect(self.GetTimeVideoResult)
        # VideoSingleton.timer.connect(self.GetTimeVideoResult)
        print("VideoSingleton.timer.connect(self.GetTimeVideoResult)")

        self.NN_Start()

    # 开始
    def NN_Start(self):
        print("九九乘法 NN_Start()")
        self.digit = 2
        global StopFlag
        global sec
        sec = 15
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec / 10), int(sec % 10))

        # 未超时和确定按钮
        self.Button_timeout_flag = False

        # 退出标志
        self.EndFlag = False

        # 设置无对错图片
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))

        # 设置提示语
        self.right_Number_LineEdit_5.setText("请填写下列空格，使得等式成立(可以有多种答案)")
        self.right_Number_LineEdit_6.setText("")

        # 设置手势识别错误次数
        self.ErrorCount = 0

        # 设置查看答案按钮不可见
        self.right_button_3.setHidden(True)

        # 设置获得按钮标志的状态
        self.GetAnswerFlag = False

        # QmutNN.lock()
        StopFlag = False
        self.timevideothread.SetVideoSingleton(False)
        # QmutNN.unlock()

        # 初始化各个编辑框的数值
        self.value1 = -1
        self.value2 = -1
        self.value3 = -1
        self.value4 = -1

        # 设置全部编辑框为不隐藏的
        self.right_Number_LineEdit_1.setHidden(False)
        self.right_Number_LineEdit_2.setHidden(False)
        self.right_Number_LineEdit_3.setHidden(False)
        self.right_Number_LineEdit_4.setHidden(False)

        self.Randomindex = random.randint(0,1)
        # [1] + [2] = [ ][ ]
        if self.Randomindex == 1:
            index = random.randint(0, 44)
            ArrayValue = Multiplication_Table_Formula[index]
            self.rightvalue = ArrayValue[2]
            self.value1 = ArrayValue[0]
            self.value2 = ArrayValue[1]
            self.value3 = 0
            self.value4 = 0

            # self.right_Number_LineEdit_1.setReadOnly(True)
            # self.right_Number_LineEdit_2.setReadOnly(True)
            # self.right_Number_LineEdit_3.setReadOnly(False)
            # self.right_Number_LineEdit_4.setReadOnly(False)
            self.SetReadOnly(self.right_Number_LineEdit_1,True)
            self.SetReadOnly(self.right_Number_LineEdit_2,True)
            self.SetReadOnly(self.right_Number_LineEdit_3,False)
            self.SetReadOnly(self.right_Number_LineEdit_4,False)


            if int(self.rightvalue/10) == 0:
                self.digit = 1
                self.right_Number_LineEdit_4.setHidden(True)
                # self.right_Number_LineEdit_4.setReadOnly(True)
                self.SetReadOnly(self.right_Number_LineEdit_4, True)

            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1,self.value1)
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2,self.value2)
            self.ChangeNumberImage(self.right_Number_LineEdit_3, 3,-1)
            self.ChangeNumberImage(self.right_Number_LineEdit_4, 4,-1)

        # [ ] + [ ] = [1][2]
        else:
            index = random.randint(0, 44)
            self.rightvalue = Multiplication_Table[index]
            self.value3 = int(self.rightvalue/10)
            self.value4 = int(self.rightvalue%10)

            # self.right_Number_LineEdit_1.setReadOnly(False)
            # self.right_Number_LineEdit_2.setReadOnly(False)
            # self.right_Number_LineEdit_3.setReadOnly(True)
            # self.right_Number_LineEdit_4.setReadOnly(True)
            self.SetReadOnly(self.right_Number_LineEdit_1,False)
            self.SetReadOnly(self.right_Number_LineEdit_2,False)
            self.SetReadOnly(self.right_Number_LineEdit_3,True)
            self.SetReadOnly(self.right_Number_LineEdit_4,True)

            if self.value3 == 0:
                self.digit = 1
                self.right_Number_LineEdit_4.setHidden(True)
                self.ChangeNumberImage(self.right_Number_LineEdit_3,3,self.value4)
            else:
                self.right_Number_LineEdit_4.setHidden(False)
                self.ChangeNumberImage(self.right_Number_LineEdit_3,3,self.value3)
                self.ChangeNumberImage(self.right_Number_LineEdit_4,4,self.value4)

            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1,self.value1)
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2,self.value2)

        # 获得当前状态下各个编辑框的状态可读?
        self.lst = [False] * 4
        self.Changelst = [False] * 4
        self.GetArrayLineEditRead()
        print("九九乘法表 NN_Start self.lst",self.lst)
        self.NN_Table_Start()

    # 设置定时器线程的槽函数
    def NN_Table_Start(self):
        self.timerthread.start()
        # self.timerthread = TimeWorkThread()
        # self.timerthread.timer.connect(self.countTime)
        # self.timerthread.end.connect(self.end)
        # self.timerthread.SignalButton.connect(self.ButtonConnect)
        # self.timerthread.start()

    # 当编辑框文本发生变化时
    def textchanged(self,right_Number_LineEdit,number):
        text = right_Number_LineEdit.text()
        print("九九乘法表 number : ",number," ",text)
        if text == "":
            return

        if not is_number(text):
            right_Number_LineEdit.setText("")
            return

        # if number == 1:
        #     self.value1 = int(text)
        # elif number == 2:
        #     self.value2 = int(text)
        # elif number == 3:
        #     self.value3 = int(text)
        # elif number == 4:
        #     self.value4 = int(text)

        if int(text)>=0 & int(text)<=9:
            self.ChangeNumberImage(right_Number_LineEdit,number,int(text))


        print("九九乘法表 before right_Number_LineEdit_1 text:",self.right_Number_LineEdit_1.text())
        right_Number_LineEdit.setText("")
        print("九九乘法表 after right_Number_LineEdit_1 text:", self.right_Number_LineEdit_1.text())

    # 线程中改变数值
    def ChangeNumberTime(self,label1,label2,a,b):
        label1.setPixmap(QPixmap("../images/number"+str(a)+".png"))
        label1.setScaledContents(True)  # 让图片自适应label大小
        label2.setPixmap(QPixmap("../images/number"+str(b)+".png"))
        label2.setScaledContents(True)  # 让图片自适应label大小

    # 改变编辑框的图片
    def ChangeNumberImage(self,right_Number_LineEdit,index,number):

        if number == -1:
            filename = "../images/空.png"
        else:
            filename = "../images/number"+str(number)+".png"
            if index == 1:
                self.value1 = int(number)
            elif index == 2:
                self.value2 = int(number)
            elif index == 3:
                self.value3 = int(number)
            elif index == 4:
                self.value4 = int(number)

        pal = right_Number_LineEdit.palette()
        pal.setBrush(QPalette.Base, QBrush(QPixmap(filename).scaled(right_Number_LineEdit.size())))
        right_Number_LineEdit.setAutoFillBackground(True)
        right_Number_LineEdit.setPalette(pal)

    # 初始化
    def init_fram(self):
        self.right_Number_LineEdit_1 = QLineEdit(self.frame)
        self.right_Number_LineEdit_1.setObjectName('right_Number')
        self.right_Number_LineEdit_2 = QLineEdit(self.frame)
        self.right_Number_LineEdit_2.setObjectName('right_Number')
        self.right_Number_LineEdit_3 = QLineEdit(self.frame)
        self.right_Number_LineEdit_3.setObjectName('right_Number')
        self.right_Number_LineEdit_4 = QLineEdit(self.frame)
        self.right_Number_LineEdit_4.setObjectName('right_Number')
        self.right_Number_LineEdit_5 = QLineEdit(self.frame)
        self.right_Number_LineEdit_5.setObjectName('right_Number_LineEdit_56')
        self.right_Number_LineEdit_6 = QLineEdit(self.frame)
        self.right_Number_LineEdit_6.setObjectName('right_Number_LineEdit_56')

        # self.right_Number_LineEdit_6.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        # self.right_Number_LineEdit_1.setStyleSheet("background:transparent;border-width:0;border-style:outset")


        self.right_label1 = QLabel(self.frame)
        self.right_label2 = QLabel(self.frame)

        self.right_Number_LineEdit_1.setGeometry(QtCore.QRect(110, 400, 140, 200))
        self.right_label1.setGeometry(QtCore.QRect(260, 450, 140, 100))
        self.right_Number_LineEdit_2.setGeometry(QtCore.QRect(410, 400, 140, 200))
        self.right_label2.setGeometry(QtCore.QRect(550, 450, 140, 100))
        self.right_Number_LineEdit_3.setGeometry(QtCore.QRect(710, 400, 140, 200))
        self.right_Number_LineEdit_4.setGeometry(QtCore.QRect(850, 400, 140, 200))
        self.right_Number_LineEdit_5.setGeometry(QtCore.QRect(150, 280, 860, 40))
        self.right_Number_LineEdit_5.setAlignment(Qt.AlignCenter)
        self.right_Number_LineEdit_5.setStyleSheet("color:white;font:32px;background:transparent;border-width:0;border-style:outset")
        self.right_Number_LineEdit_6.setGeometry(QtCore.QRect(250, 330, 650, 40))
        self.right_Number_LineEdit_6.setAlignment(Qt.AlignCenter)
        self.right_Number_LineEdit_6.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;border-style:outset")
        # self.right_Number_LineEdit_6.setText("请填写下列空格，使得等式成立")

        # self.right_Number_LineEdit_1.setAttribute(QtCore.Qt.WA_MacShowFocusRect,0)


        self.right_Number_LineEdit_1.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_2.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_3.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_4.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_1.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_1,1))
        self.right_Number_LineEdit_2.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_2,2))
        self.right_Number_LineEdit_3.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_3,3))
        self.right_Number_LineEdit_4.textChanged.connect(lambda: self.textchanged(self.right_Number_LineEdit_4,4))


        self.right_top_time_label = QLabel(self.frame)
        self.right_top_label_1 = QLabel(self.frame)
        self.right_top_label_2 = QLabel(self.frame)
        self.right_bottom_label_1 = QLabel(self.frame)


        self.right_top_time_label.setGeometry(QtCore.QRect(500, 0, 130, 140))
        self.right_top_label_1.setGeometry(QtCore.QRect(480, 140, 80, 120))
        self.right_top_label_2.setGeometry(QtCore.QRect(550, 140, 80, 120))
        self.right_bottom_label_1.setGeometry(QtCore.QRect(490, 720, 200, 140))

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

        self.right_button_2 = QtWidgets.QPushButton("退出", self.frame)
        self.right_button_2.clicked.connect(self.DeleteFram)
        self.right_button_2.setGeometry(QtCore.QRect(1050, 40, 100, 50))
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

        self.right_button_3 = QtWidgets.QPushButton("查看答案", self.frame)
        self.right_button_3.setGeometry(QtCore.QRect(910, 830, 100, 50))
        self.right_button_3.clicked.connect(self.GetAnswer)
        self.right_button_3.setStyleSheet('''
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
                border-image:url(../images/screen7.jpg);
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
        if self.value1 == -1 or self.value2 == -1 or self.value3 == -1 or self.value4 == -1:
            return False

        Avalue = self.value1 * self.value2
        if self.digit == 1:
            Bvalue = self.value3
        else:
            Bvalue = self.value3 * 10 + self.value4

        print("九九乘法表 self.value1 : ", self.value1, " self.value2 : ", self.value2)
        print("九九乘法表 self.value3 : ", self.value3, " self.value4 : ", self.value4)
        print("九九乘法表 Avalue : ",Avalue, " Bvalue : ", Bvalue)

        if Avalue == Bvalue:
            return True
        else:
            return False

    # 手势识别错误之后第一次提示
    def GetTipsValueFirst(self):
        self.right_Number_LineEdit_5.setText("手势识别回答错误，重新根据提示摆出酷酷的手势")
        # [1] + [2] = [ ][ ]
        if self.Randomindex == 1:
            cur = self.rightvalue
            if cur <= 9:
                tip2 = "请对着摄像头的红框摆出一个酷酷的手势" + str(self.firstrightvalue)
                return
            else:
                tip2 = "请对着摄像头的红框摆出第一个酷酷的手势"+ str(self.firstrightvalue)
                self.right_Number_LineEdit_6.setText(tip2)
        else:
            tip2 = "请对着摄像头的红框摆出第一个酷酷的手势" + str(self.firstleftvalue)
            self.right_Number_LineEdit_6.setText(tip2)

    # 第二次获得手势识别的结果
    def GetTipsValueSecond(self):
        # [1] + [2] = [ ][ ]
        if self.Randomindex == 1:
            cur = self.rightvalue
            if cur <= 9:
                return
            else:
                tip2 = "请对着摄像头的红框摆出第二个酷酷的手势"+ str(self.secondrightvalue)
                self.right_Number_LineEdit_6.setText(tip2)
        else:
            tip2 = "请对着摄像头的红框摆出第二个酷酷的手势" + str(self.secondleftvalue)
            self.right_Number_LineEdit_6.setText(tip2)

    # 第一次获得手势是的结果，同时保存正确的结果
    def GetTipsValue(self):
        # [1] + [2] = [ ][ ]
        if self.Randomindex == 1:
            cur = self.rightvalue
            if cur <= 9:
                self.firstrightvalue = int(cur)
                self.secondrightvalue = -1
                tip1 = "该等式不成立，正确的答案为" + str(self.firstrightvalue)
                tip2 = "请对着摄像头的红框摆出酷酷的手势"+ str(self.firstrightvalue)
                self.right_Number_LineEdit_5.setText(tip1)
                self.right_Number_LineEdit_6.setText(tip2)
            else:
                self.firstrightvalue = int(cur/10)
                self.secondrightvalue = cur%10
                tip1 = "该等式不成立，正确的答案为" + str(self.firstrightvalue) + str(self.secondrightvalue)
                tip2 = "请对着摄像头的红框摆出第一个酷酷的手势"+ str(self.firstrightvalue)
                self.right_Number_LineEdit_5.setText(tip1)
                self.right_Number_LineEdit_6.setText(tip2)
        # [ ] + [ ] = [1][2]
        else:
            cur = Multiplication_Table_Pre[self.rightvalue]
            index = 0
            if len(cur) == 1:
                self.firstleftvalue = cur[index][0]
                self.secondleftvalue = cur[index][1]
                tip1 = "该等式不成立，正确的答案为" + str(self.firstleftvalue) +" "+ str(self.secondleftvalue)
                tip2 = "请对着摄像头的红框摆出第一个酷酷的手势"+ str(self.firstleftvalue)
                self.right_Number_LineEdit_5.setText(tip1)
                self.right_Number_LineEdit_6.setText(tip2)
            else:
                index = random.randint(0,1)
                self.firstleftvalue = cur[index][0]
                self.secondleftvalue = cur[index][1]
                tip1 = "该等式不成立，正确的答案为" + str(self.firstleftvalue) +" "+ str(self.secondleftvalue)
                tip2 = "请对着摄像头的红框摆出第一个酷酷的手势"+ str(self.firstleftvalue)
                self.right_Number_LineEdit_5.setText(tip1)
                self.right_Number_LineEdit_6.setText(tip2)

    # 当手势识别错误两次之后，自动填写正确答案
    def WriteTrueValue(self):
        VideoSingleton.SetShowFlag(False)
        self.right_Number_LineEdit_5.setText("手势识别多次输入错误，请检查下手势的正确性以及周围环境")
        self.right_Number_LineEdit_6.setText("正确答案如下")
        if self.Randomindex == 1:
            cur = self.rightvalue
            if cur <= 9:
                self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, self.firstrightvalue)
                # self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, self.secondrightvalue)
            else:
                self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, self.firstrightvalue)
                self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, self.secondrightvalue)
        else:
            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, self.firstleftvalue)
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, self.secondleftvalue)

    # 通过按钮查看答案
    def GetAnswer(self):
        self.GetAnswerFlag = True
        self.timevideothread.SetVideoSingleton(True)
        VideoSingleton.SetShowFlag(False)
        QmutNN.lock()
        self.right_Number_LineEdit_5.setText("查看答案")
        self.right_Number_LineEdit_6.setText("正确答案如下")
        self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
        self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

        if self.Randomindex == 1:
            cur = self.rightvalue
            if cur <= 9:
                self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, self.firstrightvalue)
                # self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, self.secondrightvalue)
            else:
                self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, self.firstrightvalue)
                self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, self.secondrightvalue)
        else:
            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, self.firstleftvalue)
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, self.secondleftvalue)
        QmutNN.unlock()

    # 正常流程结束
    def end(self):
        global StopFlag,sec,VideoThreadEnd
        if self.IsTrue():
            self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        else:
            Button_timeout.lock()


            if self.Button_timeout_flag:
                return
            self.Button_timeout_flag = True
            self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

            # 结束定时器
            StopFlag = True

            # 开启手势识别
            VideoSingleton.SetShowFlag(True)

            # 提示语
            self.GetTipsValue()

            # 设置按钮可见
            self.right_button_3.setHidden(False)

            # 设置手势识别定时器秒数
            sec = 12

            # 填写错误之后将全部编辑框锁定
            self.right_Number_LineEdit_1.setReadOnly(False)
            self.right_Number_LineEdit_2.setReadOnly(False)
            self.right_Number_LineEdit_3.setReadOnly(False)
            self.right_Number_LineEdit_4.setReadOnly(False)

            # 获得编辑框列表需要手势识别的下标
            self.Changelst = copy.deepcopy(self.lst)
            VideoThreadEnd = False
            print("九九乘法表 QLineEditCount ", QLineEditCount)
            self.timevideothread.start()
            Button_timeout.unlock()


        self.right_button_1.setText("下一题")
        self.ButtonFlag = False

    # 确定和下一题按钮触发的事件
    def ChangeButtonStatus(self):
        global StopFlag,sec,VideoThreadEnd,QLineEditCount
        print("九九乘法表 ChangeButtonStatus")
        # 确定
        if self.ButtonFlag == True:
            print("九九乘法表 self.ButtonFlag True")
            self.right_button_1.setEnabled(False)
            self.right_button_2.setEnabled(False)
            StopFlag = True
            QmutNN.lock()
            if self.IsTrue():
                self.right_Number_LineEdit_5.setText("恭喜你，回答正确")
                self.right_Number_LineEdit_6.setText("")
                print("九九乘法表 self.ButtonFlag True self.IsTrue() True")
                self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            else:
                print("九九乘法表 self.ButtonFlag True self.IsTrue() False")
                Button_timeout.lock()
                if self.Button_timeout_flag:
                    Button_timeout.unlock()
                    QmutNN.unlock()
                    return
                self.Button_timeout_flag = True

                self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

                # 开启手势识别
                VideoSingleton.SetShowFlag(True)

                # 设置定时器秒数
                sec = 12

                # 提示语
                self.GetTipsValue()

                # 设置按钮可见
                self.right_button_3.setHidden(False)
                self.right_button_3.setEnabled(True)

                # 填写错误之后将全部编辑框锁定
                self.right_Number_LineEdit_1.setReadOnly(True)
                self.right_Number_LineEdit_2.setReadOnly(True)
                self.right_Number_LineEdit_3.setReadOnly(True)
                self.right_Number_LineEdit_4.setReadOnly(True)

                # 获得编辑框列表需要手势识别的下标
                self.Changelst = copy.deepcopy(self.lst)
                VideoThreadEnd = False
                # print("QLineEditCount ",QLineEditCount)
                self.timevideothread.start()
                Button_timeout.unlock()

            self.right_button_1.setText("下一题")
            self.ButtonFlag = False
            QmutNN.unlock()
        # 下一题
        else:
            print("九九乘法表 self.ButtonFlag False")
            if self.IsTrue():
                print("九九乘法表 self.IsTrue() True")
                self.NN_Start()
                self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
                self.right_button_1.setText("确定")
                self.ButtonFlag = True
                return

            if VideoThreadEnd:
                print("九九乘法表 VideoThreadEnd 正常结束")
                VideoThreadEnd = False
                self.NN_Start()
                self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
                self.right_button_1.setText("确定")
            else:
                self.timevideothread.SetVideoSingleton(True)
                QmutNN.lock()
                print("九九乘法表 No VideoThreadEnd 中断结束")
                self.right_button_1.setEnabled(False)
                self.right_button_2.setEnabled(False)
                self.right_button_3.setEnabled(False)
                VideoSingleton.SetShowFlag(False)
                QmutNN.unlock()
            VideoSingleton.SetShowFlag(False)
            self.ButtonFlag = True

    # 手势识别中获取结果并判断结果和流程
    ErrorCount = 0
    def GetTimeVideoResult(self,result):
        self.index = -1
        self.indexflag = True
        global QLineEditCount,VideoThreadEnd
        # print(self.Changelst)
        for i in range(0,len(self.Changelst)):
            if self.Changelst[i] == True:
                self.Changelst[i] = False
                self.index = i
                break

        if self.index == 0:
            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, result)
        elif self.index == 1:
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, result)
        elif self.index == 2:
            self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, result)
        elif self.index == 3:
            self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, result)

        for i in range(self.index,len(self.Changelst)):
            if self.Changelst[i] == True:
                self.indexflag = False

        print("九九乘法表 GetTimeVideoResult self.index", self.indexflag)
        if self.indexflag == True:
            if self.IsTrue() == False:
                if self.ErrorCount == 1:
                    # 写入正确答案
                    self.WriteTrueValue()
                    self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                    self.ErrorCount = 0

                else:
                    self.ErrorCount += 1
                    print("九九乘法表 回答错误，重新根据提示摆出酷酷的手势")

                    self.GetTipsValueFirst()
                    # self.right_Number_LineEdit_5.setText("回答错误，重新根据提示摆出酷酷的手势")

                    self.Changelst = copy.deepcopy(self.lst)
                    print("九九乘法表 GetTimeVideoResult self.Changelst",self.Changelst)
                    print("九九乘法表 GetTimeVideoResult self.lst", self.lst)

                    QmutNN.lock()
                    VideoThreadEnd = False
                    QLineEditCount = self.LineEditCount
                    QmutNN.unlock()

                    print("九九乘法表 QLineEdit",QLineEditCount)
                    print("九九乘法表 VideoThreadEnd",VideoThreadEnd)
                    print("九九乘法表 self.timevideothread.start()")
                    self.timevideothread.start()
            else:
                self.right_Number_LineEdit_5.setText("恭喜你，回答正确")
                self.right_Number_LineEdit_6.setText("")
                self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.GetTipsValueSecond()

        return

    # 获得编辑框状态数组
    def GetArrayLineEditRead(self):
        global QLineEditCount
        QLineEditCount = 0
        if self.right_Number_LineEdit_1.isReadOnly() == False:
            self.lst[0] = True
            QLineEditCount += 1
            # print("right_Number_LineEdit_1")

        if self.right_Number_LineEdit_2.isReadOnly() == False:
            self.lst[1] = True
            QLineEditCount += 1
            # print("right_Number_LineEdit_2")

        if self.right_Number_LineEdit_3.isReadOnly() == False:
            self.lst[2] = True
            QLineEditCount += 1
            # print("right_Number_LineEdit_3")

        if self.right_Number_LineEdit_4.isReadOnly() == False:
            self.lst[3] = True
            QLineEditCount += 1
            # print("right_Number_LineEdit_4")

        # print("lst ",self.lst)
        self.LineEditCount = QLineEditCount

    # 中断手势识别的定时器后触发的函数，恢复按钮同时，创建新的题目
    def VideoButtonConnect(self):

        if self.EndFlag:
            self.EndFlag = False
            return

        print("九九乘法表 VideoButtonConnect start")
        self.right_button_1.setEnabled(True)
        self.right_button_2.setEnabled(True)
        self.right_button_3.setEnabled(True)

        if self.GetAnswerFlag == True:
            return

        self.NN_Start()
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
        self.right_button_1.setText("确定")
        self.ButtonFlag = True

    # 中断定时器触发的函数，恢复按钮
    def ButtonConnect(self):
        print("九九乘法表 ButtonConnect start")
        self.right_button_1.setEnabled(True)
        self.right_button_2.setEnabled(True)
        self.right_button_3.setEnabled(True)

    # 退出按钮触发函数，初始化各个参数
    EndFlag = False
    def DeleteFram(self):
        print("九九乘法表 DeleteFram Start")
        global sec,VideoThreadEnd,StopFlag
        # 设置退出标志为True
        self.EndFlag = True

        # 手势识别非正常结束
        VideoThreadEnd = False

        # 初始化按钮标志
        self.ButtonFlag = True
        self.right_button_1.setText("确定")

        print("九九乘法表 VideoSingleton.timer.disconnect(self.GetTimeVideoResult)")
        VideoSingleton.timer.disconnect(self.GetTimeVideoResult)

        print("九九乘法表 设置结束标志")
        # 定时器结束标志
        StopFlag = True
        # 手势识别定时器结束标志
        VideoSingleton.SetShowFlag(False)
        self.timevideothread.SetVideoSingleton(True)
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec/10), int(sec%10))

        print("九九乘法表 DeleteFram End")

    def SetReadOnly(self,right_Number_LineEdit,flag):
        if flag:
            right_Number_LineEdit.setReadOnly(True)
            right_Number_LineEdit.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;border-style:outset")
        else:
            right_Number_LineEdit.setReadOnly(False)
            right_Number_LineEdit.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;")

