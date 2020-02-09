from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import random
from finger_train import *
import picture as pic
import cv2
import sys
import qtawesome

Model_Path = "../src/model/model_2019_11_20_best.hdf5"

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

Qmut = QMutex()
StopFlag = False
FingerStopFlag = False
sec = 10
thread = 0
class TimeWorkThread(QThread):
    def __init__(self):
        super().__init__()

    SignalButton = pyqtSignal()  # 恢复按钮触发函数
    timer = pyqtSignal()   # 每隔1秒发送一次信号
    end = pyqtSignal()     # 计数完成后发送一次信号
    def run(self):
        Qmut.lock()        # 加锁防止出现两个线程
        global sec
        global thread
        while True:
            # print("***********")
            if StopFlag:
                thread +=1
                print("StopFlag end thread",thread)
                break

            self.sleep(1)  # 休眠1秒
            print("TimeWorkThread StopFlag",StopFlag)
            if sec == 0:
                self.end.emit()   # 发送end信号
                break
            self.timer.emit()   # 发送timer信号
        self.SignalButton.emit()
        Qmut.unlock()

class TimeVideoThread(QThread):

    def __init__(self):
        super().__init__()

    workthread = pyqtSignal()
    timer = pyqtSignal()   # 每隔1秒发送一次信号
    # end = pyqtSignal()     # 计数完成后发送一次信号

    def EndTime(self):
        self.workthread.emit()

    def run(self):
        Qmut.lock()        # 加锁防止出现两个线程
        global sec
        sec = 10
        self.timer.emit()  # 发送timer信号

        while True:
            # if StopFlag:
            #     break

            self.sleep(1)  # 休眠1秒
            if sec == 0:
                self.EndTime()
                break
            self.timer.emit()   # 发送timer信号
        Qmut.unlock()


# 正常大小无衬线字体
font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1
# ROI框的显示位置
x0 = 330
y0 = 40
# 录制的手势图片大小
width = 300
height = 300


class VideoThread(QThread):
    timer = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.result = 0

    def work(self):
        self.timer.emit(int(self.result))

    def Getbinary(self,frame, x0, y0, width, height, finger_model):
        # 得到处理后的照片
        res = pic.new_binaryMask(frame, x0, y0, width, height)

        out = 0
        """这里可以插入代码调用网络"""
        test_image = res
        test_image = cv.resize(test_image, (300, 300))
        test_image = np.array(test_image, dtype='f')
        test_image = test_image / 255.0
        test_image = test_image.reshape([-1, 300, 300, 1])
        pdt = finger_model.predict(test_image)
        out = np.argmax(pdt, axis=1)
        cv2.putText(frame, "the finger is: %d" % out, (x0, y0), font, fontsize, (0, 255, 0))  # 标注字体
        return out

    def startvideo(self,finger_model):
        # 开启摄像头
        cap = cv2.VideoCapture(0)

        self.lst = [0] * 10
        self.index = 0

        while (True):
            # 读帧
            ret, frame = cap.read()
            # 图像翻转
            frame = cv2.flip(frame, 2)
            # 显示ROI区域  #调用函数

            # 获得图像预测的数值
            VideoNumber = self.Getbinary(frame, x0, y0, width, height, finger_model)

            if self.index != 10:
                self.lst[self.index] = int(VideoNumber)
            else:
                self.index = 0
                self.lst[self.index] = int(VideoNumber)

            self.index += 1
            self.result = np.argmax(np.bincount(self.lst))
            print("lst",self.lst," maxnumber:",self.result)

            # 等待键盘输入
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            cv2.imshow("frame", frame)

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        global Model_Path
        finger_model = loadCNN()
        finger_model.load_weights(Model_Path)
        self.startvideo(finger_model)

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

    # 正常流程结束
    def end(self):
        if self.IsTrue():
            self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        # self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
        # self.right_bottom_label_1.setScaledContents(True)
        self.right_button_1.setText("下一题")
        self.ButtonFlag = False

    # 开始
    def NN_Start(self):
        # self.right_button_1.setHidden(True)
        # self.right_button_1.setEnabled(False)
        # self.right_button_1.clicked.disconnect()
        self.digit = 2
        global StopFlag
        global sec
        sec = 10
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec / 10), int(sec % 10))

        # Qmut.lock()
        StopFlag = False
        # Qmut.unlock()

        # self.right_button_1.clicked.connect(self.ChangeButtonStatus)
        # self.right_button_1.setHidden(False)
        # self.right_button_1.setEnabled(True)
        # self.right_button_1.clicked.connect(self.ChangeButtonStatus)

        self.value1 = -1
        self.value2 = -1
        self.value3 = -1
        self.value4 = -1

        self.right_Number_LineEdit_1.setHidden(False)
        self.right_Number_LineEdit_2.setHidden(False)
        self.right_Number_LineEdit_3.setHidden(False)
        self.right_Number_LineEdit_4.setHidden(False)

        index = random.randint(0,1)
        if index == 1:
            index = random.randint(0, 44)
            ArrayValue = Multiplication_Table_Formula[index]
            self.value = ArrayValue[2]
            self.value1 = ArrayValue[0]
            self.value2 = ArrayValue[1]
            self.value3 = 0
            self.value4 = 0

            if int(self.value/10) == 0:
                self.digit = 1
                self.right_Number_LineEdit_4.setHidden(True)

            self.ChangeNumberImage(self.right_Number_LineEdit_1, 1,self.value1)
            self.ChangeNumberImage(self.right_Number_LineEdit_2, 2,self.value2)
            self.ChangeNumberImage(self.right_Number_LineEdit_3, 3,-1)
            self.ChangeNumberImage(self.right_Number_LineEdit_4, 4,-1)

            self.right_Number_LineEdit_1.setReadOnly(True)
            self.right_Number_LineEdit_2.setReadOnly(True)
            self.right_Number_LineEdit_3.setReadOnly(False)
            self.right_Number_LineEdit_4.setReadOnly(False)
            self.NN_Table_Start()
        else:


            index = random.randint(0, 44)
            self.value = Multiplication_Table[index]
            self.value3 = int(self.value/10)
            self.value4 = int(self.value%10)

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
            self.right_Number_LineEdit_1.setReadOnly(False)
            self.right_Number_LineEdit_2.setReadOnly(False)
            self.right_Number_LineEdit_3.setReadOnly(True)
            self.right_Number_LineEdit_4.setReadOnly(True)

            self.NN_Table_Start()

    # def NN_Start(self):
    #     self.videothread = VideoThread()
    #     self.videothread.start()

    def NN_Table_Start(self):
        self.timerthread = TimeWorkThread()
        self.timerthread.timer.connect(self.countTime)
        self.timerthread.end.connect(self.end)
        self.timerthread.SignalButton.connect(self.ButtonConnect)
        self.timerthread.start()



    def NN_Table_Start_Time(self):
        self.timerthread = TimeVideoThread()
        self.timerthread.timer.connect(self.countTime)
        self.timerthread.end.connect(self.end)
        self.timerthread.start()

    # 当编辑框文本发生变化时
    def textchanged(self,right_Number_LineEdit,number):
        text = right_Number_LineEdit.text()
        print("number : ",number," ",text)
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
        if self.digit == 1:
            Bvalue = self.value3
        else:
            Bvalue = self.value3 * 10 + self.value4

        print("self.value1 : ", self.value1, " self.value2 : ", self.value2)
        print("self.value3 : ", self.value3, " self.value4 : ", self.value4)
        print("Avalue : ",Avalue, " Bvalue : ", Bvalue)

        if Avalue == Bvalue:
            return True
        else:
            return False

    OnceButtonFlag = True
    # 确定和下一题按钮触发的事件
    def ChangeButtonStatus(self):
        if self.ButtonFlag == True:
            self.right_button_1.setEnabled(False)
            if self.IsTrue():
                self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            else:
                self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

                # 开启手势识别
                self.videothread = VideoThread()
                self.videothread.timer.connect(self.GetTimeVideoResult)
                self.videothread.start()
                self.timevideothread = TimeVideoThread()
                self.timevideothread.timer.connect(self.countTime)
                self.timevideothread.workthread.connect(self.videothread.work)
                self.timevideothread.start()

            global StopFlag
            StopFlag = True

            self.right_button_1.setText("下一题")
            self.ButtonFlag = False
        else:
            # if self.OnceButtonFlag == True:
            #     return

            # self.OnceButtonFlag = True
            print("**************False***********")
            # self.right_button_1.disconnect()
            #
            self.NN_Start()
            self.right_bottom_label_1.setPixmap(QPixmap("../images/空号.png"))
            self.right_button_1.setText("确定")
            self.ButtonFlag = True
            # self.right_button_1.disconnect()

    def GetTimeVideoResult(self,result):
        if self.right_Number_LineEdit_1.isReadOnly() == False:
            self.ChangeNumberImage(self.right_Number_LineEdit_1,1,result)
            self.right_Number_LineEdit_1.setReadOnly(True)
        elif self.right_Number_LineEdit_2.isReadOnly() == False:
            self.ChangeNumberImage(self.right_Number_LineEdit_2,2,result)
            self.right_Number_LineEdit_2.setReadOnly(True)
        elif self.right_Number_LineEdit_3.isReadOnly() == False:
            self.ChangeNumberImage(self.right_Number_LineEdit_3,3,result)
            self.right_Number_LineEdit_3.setReadOnly(True)
        elif self.right_Number_LineEdit_4.isReadOnly() == False:
            self.ChangeNumberImage(self.right_Number_LineEdit_4,4,result)
            self.right_Number_LineEdit_4.setReadOnly(True)

        return

    def ButtonConnect(self):
        # self.right_button_1.connect(self.ChangeButtonStatus)

        self.right_button_1.setEnabled(True)
        print("**************True***********")
    def DeleteFram(self):
        global StopFlag
        global sec
        self.ButtonFlag = True
        StopFlag = True
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空号.png"))
        self.ChangeNumberTime(self.right_top_label_1, self.right_top_label_2, int(sec/10), int(sec%10))

