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

# 加号 2 - 18
Add_Table_Pre = { 2 : [[1,1]], 3 : [[1,2]], 4:[[2,2],[1,3]], 5 : [[1,4],[2,3]], 6 : [[1,5],[2,4],[3,3]],
                  7 : [[1,6],[2,5],[3,4]], 8 : [[1,7],[2,6],[3,5],[4,4]], 9 : [[1,8],[2,7],[3,6],[4,5]],
                  10 : [[1,9],[2,8],[3,7],[4,6],[5,5]], 11 : [[2,9],[3,8],[4,7],[5,6]], 12 : [[3,9],[4,8],[5,7],[6,6]],
                  13 : [[4,9],[5,8],[6,7]], 14 : [[5,9],[6,8],[7,7]], 15 : [[6,9],[7,8]], 16 : [[7,9],[8,8]],
                  17 : [[8,9]], 18 : [[9,9]]
                  }

# 减号
Minus_Table_Pre = { 2 : [[1,1]], 3 : [[1,2],[2,1]], 4 : [[1,3],[2,2],[3,1]], 5 : [[1,4],[2,3],[3,2],[4,1]],
                    6 : [[1,5],[2,4],[3,3],[4,2],[5,1]], 7 : [[1,6],[2,5],[3,4],[4,3],[5,2],[6,1]],
                    8 : [[1,7],[2,6],[3,5],[4,4],[5,3],[6,2],[7,1]], 9: [[1,8],[2,7],[3,6],[4,5],[5,4],[6,3],[7,2],[8,1]]

}

NExamMutx = QMutex()



# 正常考试停止信号
NExamStopFlag = False

# 考试时间
Nsec = 180
class NormalExamTimeWorkThread(QThread):
    def __init__(self):
        super().__init__()

    SignalButton = pyqtSignal()  # 恢复按钮触发函数
    timer = pyqtSignal()   # 每隔1秒发送一次信号
    end = pyqtSignal()     # 计数完成后发送一次信号
    def run(self):
        print("NormalExamTimeWorkThread run")
        NExamMutx.lock()        # 加锁防止出现两个线程
        global NExamStopFlag,Nsec
        print("NExamStopFlag")
        while True:
            print("NormalExamTimeWorkThread Nsec", Nsec)
            if NExamStopFlag:
                break

            self.sleep(1)  # 休眠1秒

            if NExamStopFlag:
                break
            if Nsec == 0:
                self.end.emit()   # 发送end信号
                NExamMutx.unlock()
                return
            self.timer.emit()   # 发送timer信号
        print("NormalExamTimeWorkThread end")
        self.SignalButton.emit()
        NExamMutx.unlock()

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

class Examination(object):
    def __init__(self,parents):
        super().__init__()
        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(1200, 900)

        self.ButtonFlag = True
        self.init_frame(parents)

        self.frame1 = QWidget(parents)
        self.frame1.setObjectName("Frame1")
        self.frame1.resize(1200, 900)
        self.frame1.setFixedSize(1200, 900)
        self.init_frame1(parents)

        self.frame2 = QWidget(parents)
        self.frame2.setObjectName("Frame2")
        self.frame2.resize(1200, 900)
        self.frame2.setFixedSize(1200, 900)
        self.init_frame2(parents)

        self.frame.setVisible(False)
        self.frame1.setVisible(False)
        self.frame2.setVisible(False)


    def ShowSubmitDialog(self):
        self.SubmitDialog = QDialog()

        self.SubmitDialog.resize(400,83)
        self.SubmitDialog.setFixedSize(400,83)

        self.SubmitEdit = QLineEdit(self.SubmitDialog)
        self.SubmitEdit.setReadOnly(True)
        self.SubmitEdit.resize(400,50)
        self.SubmitEdit.setFixedSize(400, 50)

        self.SubmitEdit.setStyleSheet("color:white;background:transparent;border-width:0;border-style:outset;font:20px")
        self.SubmitEdit.setAlignment(Qt.AlignCenter)
        self.SubmitEdit.setText(self.tip)

        self.SubmitHLayout = QtWidgets.QWidget(self.SubmitDialog)
        # self.HLayout.setGeometry(QtCore.QRect(0, 0, 300, 50))
        self.Submitbutton1 = QPushButton('确定',self.SubmitHLayout)
        self.Submitbutton1.setObjectName("DialogButton")
        self.Submitbutton2 = QPushButton('取消', self.SubmitHLayout)
        self.Submitbutton2.setObjectName("DialogButton")

        self.Submitbutton1.clicked.connect(self.SubmitDialog.close)
        self.Submitbutton1.clicked.connect(self.GetScore)
        self.Submitbutton2.clicked.connect(self.SubmitDialog.close)

        self.SubmitDialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.SubmitDialog.setWindowOpacity(1)  # 设置窗口透明度
        # self.SubmitDialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.Submitbutton1.setFixedSize(100,30)
        self.Submitbutton2.setFixedSize(100,30)

        self.Submitbutton1.move(100,50)
        self.Submitbutton2.move(200, 50)

        self.SubmitDialog.setObjectName("ExDialog")


        self.SubmitDialog.setStyleSheet('''
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

        self.SubmitHLayout.setStyleSheet('''
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

        self.SubmitDialog.setWindowTitle('提交试卷')
        self.SubmitDialog.setWindowModality(Qt.ApplicationModal)

        self.SubmitDialog.exec()


    def ShowDialog(self):
        self.Exdialog = QDialog()

        self.Exdialog.resize(300,100)
        self.Exdialog.setFixedSize(300,100)

        self.HLayout = QtWidgets.QWidget(self.Exdialog)
        self.HLayout.resize(300,100)
        self.HLayout.setFixedSize(300,100)
        self.HLayout.setObjectName("HLayout")
        # self.HLayout.setGeometry(QtCore.QRect(0, 0, 300, 50))
        self.button1 = QPushButton('容易',self.HLayout)
        self.button1.setObjectName("DialogButton")
        self.button2 = QPushButton('中等', self.HLayout)
        self.button2.setObjectName("DialogButton")
        self.button3 = QPushButton('困难', self.HLayout)
        self.button3.setObjectName("DialogButton")

        self.button1.clicked.connect(self.Exdialog.close)
        self.button1.clicked.connect(lambda :self.SetDifficulty(2))
        self.button2.clicked.connect(self.Exdialog.close)
        self.button2.clicked.connect(lambda: self.SetDifficulty(1))
        self.button3.clicked.connect(self.Exdialog.close)
        self.button3.clicked.connect(lambda: self.SetDifficulty(1))

        self.Exdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.Exdialog.setWindowOpacity(1)  # 设置窗口透明度
        self.Exdialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.button1.setFixedSize(100,50)
        self.button2.setFixedSize(100,50)
        self.button3.setFixedSize(100,50)

        self.button1.move(0,30)
        self.button2.move(100, 30)
        self.button3.move(200, 30)

        self.Exdialog.setObjectName("ExDialog")


        self.Exdialog.setStyleSheet('''
        QWidget#HLayout{
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

    # 开始正常开始
    FirstNExam = True
    def NormalExam(self):
        self.frame.setVisible(False)
        self.frame1.setVisible(True)

        # 设置线程停止标志
        global NExamStopFlag
        NExamStopFlag = False

        # 非观察模式
        self.ViewFlag = False

        if self.FirstNExam:
            self.NEtimeworkthread = NormalExamTimeWorkThread()
            self.NEtimeworkthread.timer.connect(self.countTime)
            self.NEtimeworkthread.end.connect(self.GetScore)
            self.NEtimeworkthread.SignalButton.connect(self.GetScore)
            self.FirstNExam = False

        # 获得题目
        self.NormalExamQuestion()

        # 当前题目下标
        self.QuestionIndex = 0

        # 显示题目
        self.ShowExam()

        # 开始定时器
        self.NEtimeworkthread.start()


    # 考试过程页面
    def init_frame1(self,parents):
        self.right_Number_LineEdit_1 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_1.setObjectName('right_Number')
        self.right_Number_LineEdit_2 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_2.setObjectName('right_Number')
        self.right_Number_LineEdit_3 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_3.setObjectName('right_Number')
        self.right_Number_LineEdit_4 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_4.setObjectName('right_Number')
        self.right_Number_LineEdit_5 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_5.setObjectName('right_Number_LineEdit_56')
        self.right_Number_LineEdit_6 = QLineEdit(self.frame1)
        self.right_Number_LineEdit_6.setObjectName('right_Number_LineEdit_56')
        self.right_label1 = QLabel(self.frame1)
        self.right_label2 = QLabel(self.frame1)

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


        self.right_top_time_label = QLabel(self.frame1)
        self.right_top_label_1 = QLabel(self.frame1)
        self.right_top_label_2 = QLabel(self.frame1)
        self.right_top_label_3 = QLabel(self.frame1)
        self.right_bottom_label_1 = QLabel(self.frame1)


        self.right_top_time_label.setGeometry(QtCore.QRect(500, 0, 130, 140))
        self.right_top_label_1.setGeometry(QtCore.QRect(440, 140, 80, 120))
        self.right_top_label_2.setGeometry(QtCore.QRect(510, 140, 80, 120))
        self.right_top_label_3.setGeometry(QtCore.QRect(585, 140, 80, 120))
        self.right_bottom_label_1.setGeometry(QtCore.QRect(490, 720, 200, 140))
        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(../images/number2.png")
        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(:../images/number2.png);\n""background-attachment:fixed;\n""background-repeat:none;\n""background-position:center")

        self.right_top_time_label.setPixmap(QPixmap("../images/time.png"))
        self.right_top_time_label.setScaledContents(True)  # 让图片自适应label大小


        self.right_top_label_1.setPixmap(QPixmap("../images/number1.png"))
        self.right_top_label_1.setScaledContents(True)  # 让图片自适应label大小

        self.right_top_label_2.setPixmap(QPixmap("../images/number8.png"))
        self.right_top_label_2.setScaledContents(True)  # 让图片自适应label大小

        self.right_top_label_3.setPixmap(QPixmap("../images/number0.png"))
        self.right_top_label_3.setScaledContents(True)  # 让图片自适应label大小

        # self.right_label1.setToolTip('这是一个乘号标签')
        # self.right_label1.setPixmap(QPixmap("../images/乘号.png"))
        # self.right_label1.setScaledContents(True)  # 让图片自适应label大小

        self.right_label2.setToolTip('这是一个等号标签')
        self.right_label2.setPixmap(QPixmap("../images/等号.png"))
        self.right_label2.setScaledContents(True)  # 让图片自适应label大小2

        self.right_button_1 = QtWidgets.QPushButton("下一题", self.frame1)
        self.right_button_1.setGeometry(QtCore.QRect(1050, 830, 100, 50))
        self.right_button_1.clicked.connect(self.NextShowExam)
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

        self.right_button_3 = QtWidgets.QPushButton("上一题", self.frame1)
        self.right_button_3.setGeometry(QtCore.QRect(50, 830, 100, 50))
        self.right_button_3.clicked.connect(self.PreShowExam)
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


        self.right_button_2 = QtWidgets.QPushButton("提交试卷", self.frame1)
        self.right_button_2.clicked.connect(self.SubmitExam)
        self.right_button_2.setGeometry(QtCore.QRect(1050, 50, 100, 50))
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


        self.frame1.setStyleSheet('''
            QWidget#Frame1{
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

    # 考试主菜单
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 200, 300, 600))
        self.verticalLayoutWidget.setObjectName("ButtonWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("ButtonLayout")

        self.pushButton_1 = QtWidgets.QPushButton("正常考试模式", self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("HomeButton")
        self.pushButton_1.setIcon(QIcon("../images/考试.png"))
        self.pushButton_1.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_1)
        self.pushButton_1.clicked.connect(self.NormalExam)


        self.pushButton_2 = QtWidgets.QPushButton("手势识别模式", self.verticalLayoutWidget)
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

        self.pushButton_3.clicked.connect(self.ShowDialog)

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

    # 考试结束页面
    correct = 0     # 正确的题目数
    score = 0       # 分数
    def init_frame2(self,parents):
        self.frame2_QlineEdit1 = QLineEdit(self.frame2)
        self.frame2_QlineEdit2 = QLineEdit(self.frame2)
        self.frame2_button1 = QPushButton("查看题目",self.frame2)
        self.frame2_button2 = QPushButton("回主菜单",self.frame2)

        self.frame2_QlineEdit1.setGeometry(QtCore.QRect(150, 300, 860, 40))
        self.frame2_QlineEdit1.setAlignment(Qt.AlignCenter)
        self.frame2_QlineEdit1.setStyleSheet("color:white;font:32px;background:transparent;border-width:0;border-style:outset")
        self.frame2_QlineEdit2.setGeometry(QtCore.QRect(250, 380, 650, 40))
        self.frame2_QlineEdit2.setAlignment(Qt.AlignCenter)
        self.frame2_QlineEdit2.setStyleSheet("color:white;font:32px;background:transparent;border-width:0;border-style:outset")


        self.frame2_button1.setGeometry(QtCore.QRect(300, 630, 280, 50))
        self.frame2_button2.setGeometry(QtCore.QRect(600, 630, 280, 50))
        self.frame2_button1.clicked.connect(self.ViewQuestion)
        self.frame2_button2.clicked.connect(self.BackMain)


        self.frame2.setStyleSheet('''
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
            
            QWidget#Frame2{
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

    ViewFlag = False
    def ViewQuestion(self):
        # ViewStart()
        self.ViewFlag =True
        self.QuestionIndex = 0

        self.ShowExam()

        return

    def BackMain(self):
        self.frame2.setVisible(False)
        self.frame1.setVisible(False)
        self.frame.setVisible(True)


    # ********************************方法****************************

    # 0-Easy 1-Medium 2-difficult
    Difficulty = 0
    # Easy-180  Medium-120   difficult-180
    Timing = 180
    # Number of questions
    NumberQuestions = 10
    def SetDifficulty(self,result):
        global Nsec
        self.Difficulty = result
        print("Difficulty :",self.Difficulty)
        if self.Difficulty == 0 :
            self.Timing = 180
        elif self.Difficulty == 1:
            self.Timing = 120
        elif self.Difficulty == 2:
            self.Timing = 60

        Nsec = self.Timing

        if Nsec <= 9:
            self.ChangeNumberTime(-1,0,Nsec)
        elif Nsec > 9 and Nsec <= 99:
            # print("Nsec>9 and <99 ",Nsec)
            a = int(Nsec / 10)
            b = Nsec % 10
            self.ChangeNumberTime(-1,a, b)
            self.ChangeNumberTime(-1,a, b)
        elif Nsec > 99:
            # print("Nsec>99", Nsec)
            a = int(Nsec / 100)
            b = int(int(Nsec%100) / 10)
            c = int(int(Nsec%100)%10)
            print("a,b,c",a,b,c)
            self.ChangeNumberTime(a,b,c)

        # print("SetDifficulty() Nsec",Nsec)


    # 获得分数
    def GetScore(self):
        global NExamStopFlag
        NExamStopFlag = True

        NExamMutx.lock()

        if self.QuestionIndex == self.NumberQuestions-1:
            self.IsTrue()


        self.correct = 0

        for i in range(0,len(self.NEAnswerCur)):
            if self.NEAnswerCur[i] == 1:
                self.correct += 1

        self.score = int(100*self.correct/self.NumberQuestions)

        print("correct",self.correct, "score",self.score)

        self.tip1 = "本次一共有"+ str(self.NumberQuestions)+"题，回答正确为"+str(self.correct)+"道"
        self.frame2_QlineEdit1.setText(self.tip1)
        self.tip2 = "你的得分为:"+str(self.score)+"分"
        self.frame2_QlineEdit2.setText(self.tip2)

        self.frame.setVisible(False)
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

        NExamMutx.unlock()
        return

    # 提交试卷
    def SubmitExam(self):
        self.IsTrue()
        for i in range(0,len(self.NEQuestionCur)-1):
            if self.NEAnswerCur[i] == 2:
                # 弹窗
                print("之前的题目没做完")
                self.tip = "还有题目没做完，是否要提交试卷"
                self.ShowSubmitDialog()
                return

        if self.QuestionIndex == self.NumberQuestions-1:
            for i in range(0,len(self.NEQuestionCur[self.QuestionIndex])):
                if self.NEQuestionCur[self.QuestionIndex][i] == -1:
                    print("当前题目没做完")
                    self.tip = "还有题目没做完，是否要提交试卷"
                    self.ShowSubmitDialog()
                    return

        # 弹窗,确定提交
        print("题目全部做完")
        self.tip = "是否确定要提交试卷"
        self.ShowSubmitDialog()

    # 计数器
    def countTime(self):
        global Nsec
        print()

        Nsec -= 1
        if Nsec < 0:
            return
        elif Nsec <= 9:
            self.ChangeNumberTime(-1,0,Nsec)
        elif Nsec > 9 and Nsec <= 99:
            # print("Nsec>9 and <99 ",Nsec)
            a = int(Nsec / 10)
            b = Nsec % 10
            self.ChangeNumberTime(-1,a, b)
            self.ChangeNumberTime(-1,a, b)
        elif Nsec > 99:
            # print("Nsec>99", Nsec)
            a = int(Nsec / 100)
            b = int(int(Nsec%100) / 10)
            c = int(int(Nsec%100)%10)
            # print("a,b,c",a,b,c)
            self.ChangeNumberTime(a,b,c)

    # 获得考试题目
    # 答案
    NEQuestion = []
    # 题目现状
    NEQuestionCur = []
    # 题目正确 0-false,1-true,2-no run
    NEAnswerCur = []
    # 编辑框状态
    NEStatus = []
    def NormalExamQuestion(self):
        # 答案
        self.NEQuestion = []
        # 题目现状
        self.NEQuestionCur = []
        # 题目正确 0-false,1-true,2-no run
        self.NEAnswerCur = []
        # 编辑框状态
        self.NEStatus = []

        count = self.NumberQuestions
        while count:
            i = random.randint(0,4)
            # 加法
            if i == 0:
                self.value = random.randint(2,18)
                self.formula = Add_Table_Pre[self.value]
                self.indexrand = random.randint(0,len(self.formula)-1)
                self.firstvalue = self.formula[self.indexrand][0]
                self.secondvalue = self.formula[self.indexrand][1]
                if self.value >= 10:
                    self.thirdvalue = int(self.value/10)
                    self.fourthvalue = self.value%10
                else:
                    self.thirdvalue = self.value
                    self.fourthvalue = -2     # -2 表示不占位


                self.symbol = '+'
            elif i == 1:
                self.value = random.randint(2,9)
                self.formula = Minus_Table_Pre[self.value]
                self.indexrand = random.randint(0,len(self.formula)-1)
                self.firstvalue = self.value
                self.secondvalue = self.formula[self.indexrand][0]
                self.thirdvalue = self.formula[self.indexrand][1]
                self.fourthvalue = -2
                self.symbol = '-'
            elif i > 1 :
                self.value = random.randint(0,44)
                self.value = Multiplication_Table_Formula[self.value]
                self.firstvalue = self.value[0]
                self.secondvalue = self.value[1]

                if self.value[2] >= 10:
                    self.thirdvalue = int(self.value[2]/10)
                    self.fourthvalue = self.value[2] % 10
                else:
                    self.thirdvalue = self.value[2]
                    self.fourthvalue = -2     # -2 表示不占位
                self.symbol = '*'

            cur = []
            cur.append(self.firstvalue)
            cur.append(self.secondvalue)
            cur.append(self.thirdvalue)
            cur.append(self.fourthvalue)
            cur.append(self.symbol)

            ncur = copy.deepcopy(cur)
            ncurindex = random.randint(0, 2)
            ncur[ncurindex] = -1
            if ncurindex == 2:
                if cur[3] != -2:  # 如果是二位数，要将fourthvalue置位-1
                    ncur[3] = -1

            curStatu = []
            curStatu.append(True if ncur[0] == -1 else False)
            curStatu.append(True if ncur[1] == -1 else False)
            curStatu.append(True if ncur[2] == -1 else False)
            curStatu.append(True if ncur[3] == -1 else False)

            self.NEQuestion.append(cur)
            self.NEQuestionCur.append(ncur)
            self.NEAnswerCur.append(2)
            self.NEStatus.append(curStatu)
            count -= 1

        print("self.NEQuestion",self.NEQuestion)
        print("self.NEQuestionCur",self.NEQuestionCur)
        print("self.NEAnswerCur", self.NEAnswerCur)
        print("self.NEStatus", self.NEStatus)

    # 下一题按钮
    def NextShowExam(self):
        print("IsTrue()")
        self.IsTrue()

        self.QuestionIndex += 1
        print("ShowExam()")
        self.ShowExam()
        # print("self.NEQuestionCur ",self.NEQuestionCur)
        # print("self.NEStatus ",self.NEStatus)

        print("self.NEQuestionCur",self.NEQuestionCur)
        print("self.NEAnswerCur", self.NEAnswerCur)
        print("self.NEStatus", self.NEStatus)

    # 上一题按钮
    def PreShowExam(self):
        print("IsTrue()")

        self.IsTrue()

        self.QuestionIndex -= 1

        print("ShowExam()")
        self.ShowExam()

        print("self.NEQuestionCur",self.NEQuestionCur)
        print("self.NEAnswerCur", self.NEAnswerCur)
        print("self.NEStatus", self.NEStatus)

    # 开始显示
    def ShowExam(self):
        # 判断是否为第一题，第一题没有上一题
        if self.QuestionIndex == 0:
            self.right_button_3.setHidden(True)
        else:
            self.right_button_3.setHidden(False)

        # 判断为最后一题，最后一题没有下一题
        if self.QuestionIndex == self.NumberQuestions-1:
            self.right_button_1.setHidden(True)
        else:
            self.right_button_1.setHidden(False)

        if self.ViewFlag:
            self.ViewQLineEdit()
        else:
            self.ShowQLineEdit()

    # 当前题目判断是否正确
    def IsTrue(self):
        firstvalue = self.NEQuestionCur[self.QuestionIndex][0]
        secondvalue = self.NEQuestionCur[self.QuestionIndex][1]
        thirdvalue = self.NEQuestionCur[self.QuestionIndex][2]
        fourthvalue = self.NEQuestionCur[self.QuestionIndex][3]
        symbol = self.NEQuestionCur[self.QuestionIndex][4]

        # flag
        self.Aflag = False
        for i in range(0,len(self.NEQuestionCur[self.QuestionIndex])):
            if self.NEQuestionCur[self.QuestionIndex][i] == -1:
                self.Aflag = True

        if self.Aflag:
            self.NEAnswerCur[self.QuestionIndex] = 2
            return False


        if symbol == '+':
            if fourthvalue == -2:
                if firstvalue + secondvalue == thirdvalue:
                    self.NEAnswerCur[self.QuestionIndex] = 1
                    return True
                else:
                    self.NEAnswerCur[self.QuestionIndex] = 0
                    return False

            else:
                if firstvalue + secondvalue == thirdvalue*10 + fourthvalue :
                    self.NEAnswerCur[self.QuestionIndex] = 1
                    return True
                else:
                    self.NEAnswerCur[self.QuestionIndex] = 0
                    return False

        elif symbol == '-':
            if firstvalue - secondvalue == thirdvalue:
                self.NEAnswerCur[self.QuestionIndex] = 1
                return True
            else:
                self.NEAnswerCur[self.QuestionIndex] = 0
                return False

        elif symbol == '*':
            if fourthvalue == -2:
                if firstvalue * secondvalue == thirdvalue:
                    self.NEAnswerCur[self.QuestionIndex] = 1
                    return True
                else:
                    self.NEAnswerCur[self.QuestionIndex] = 0
                    return False

            else:
                if firstvalue * secondvalue == thirdvalue * 10 + fourthvalue:
                    self.NEAnswerCur[self.QuestionIndex] = 1
                    return True
                else:
                    self.NEAnswerCur[self.QuestionIndex] = 0
                    return False

    # 编辑框文本改变
    def textchanged(self,right_Number_LineEdit,number):
        text = right_Number_LineEdit.text()
        print("number : ",number," ",text)
        if text == "":
            return

        if not is_number(text):
            right_Number_LineEdit.setText("")
            return

        # 给当前的题目下的编辑框赋值
        if number == 4:
            if self.NEQuestionCur[self.QuestionIndex][number-1] == -2:
                right_Number_LineEdit.setText("")
                return

        self.NEQuestionCur[self.QuestionIndex][number-1] = int(text)


        if int(text)>=0 & int(text)<=9:
            self.ChangeNumberImage(right_Number_LineEdit,int(text))


        print("before right_Number_LineEdit text:",right_Number_LineEdit.text())
        right_Number_LineEdit.setText("")
        print("after right_Number_LineEdit text:", right_Number_LineEdit.text())

    # 修改编辑框的照片,同时取值
    def ChangeNumberImage(self,right_Number_LineEdit,number):

        if number == -2:
            return

        if number == -1:
            filename = "../images/空.png"
        else:
            filename = "../images/number"+str(number)+".png"


        # self.NEQuestionCur[self.QuestionIndex][2] = int(number)

        pal = right_Number_LineEdit.palette()
        pal.setBrush(QPalette.Base, QBrush(QPixmap(filename).scaled(right_Number_LineEdit.size())))
        right_Number_LineEdit.setAutoFillBackground(True)
        right_Number_LineEdit.setPalette(pal)

    # 查看题目
    def ViewQLineEdit(self):
        return

    # 显示题目
    def ShowQLineEdit(self):
        print("ShowQLineEdit() start")

        self.right_Number_LineEdit_1.setReadOnly(True)
        self.right_Number_LineEdit_2.setReadOnly(True)
        self.right_Number_LineEdit_3.setReadOnly(True)
        self.right_Number_LineEdit_4.setReadOnly(True)


        for i in range(0, len(self.NEStatus[self.QuestionIndex])):
            print("i : ", i)
            if self.NEStatus[self.QuestionIndex][i] == True:
                if i == 0:
                    self.right_Number_LineEdit_1.setReadOnly(False)
                if i == 1:
                    self.right_Number_LineEdit_2.setReadOnly(False)
                if i == 2:
                    self.right_Number_LineEdit_3.setReadOnly(False)
                if i == 3:
                    self.right_Number_LineEdit_4.setReadOnly(False)

        lst = self.NEQuestionCur[self.QuestionIndex]
        firstvalue = lst[0]
        secondvalue = lst[1]
        thirdvalue = lst[2]
        fourthvalue = lst[3]
        symbol = lst[4]

        if symbol == '+':
            self.right_label1.setToolTip('这是一个加号标签')
            self.right_label1.setPixmap(QPixmap("../images/加号.png"))
            self.right_label1.setScaledContents(True)  # 让图片自适应label大小
        elif symbol == '-':
            self.right_label1.setToolTip('这是一个减号标签')
            self.right_label1.setPixmap(QPixmap("../images/减号.png"))
            self.right_label1.setScaledContents(True)  # 让图片自适应label大小
        elif symbol == '*':
            self.right_label1.setToolTip('这是一个乘号标签')
            self.right_label1.setPixmap(QPixmap("../images/乘号.png"))
            self.right_label1.setScaledContents(True)  # 让图片自适应label大小


        self.ChangeNumberImage(self.right_Number_LineEdit_1,firstvalue)
        self.ChangeNumberImage(self.right_Number_LineEdit_2,secondvalue)

        if fourthvalue != -2:
            self.right_Number_LineEdit_4.setHidden(False)
        else:
            self.right_Number_LineEdit_4.setHidden(True)


        self.ChangeNumberImage(self.right_Number_LineEdit_3,thirdvalue)
        self.ChangeNumberImage(self.right_Number_LineEdit_4,fourthvalue)

        print("ShowQLineEdit() end")

    # 改变时间
    def ChangeNumberTime(self,a,b,c):
        if a != -1:
            self.right_top_label_1.setPixmap(QPixmap("../images/number"+str(a)+".png"))
            self.right_top_label_1.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.right_top_label_1.setPixmap(QPixmap("../images/空.png"))
            self.right_top_label_1.setScaledContents(True)  # 让图片自适应label大小


        if b != -1:
            self.right_top_label_2.setPixmap(QPixmap("../images/number"+str(b)+".png"))
            self.right_top_label_2.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.right_top_label_2.setPixmap(QPixmap("../images/空.png"))
            self.right_top_label_2.setScaledContents(True)  # 让图片自适应label大小

        if c != -1:
            self.right_top_label_3.setPixmap(QPixmap("../images/number"+str(c)+".png"))
            self.right_top_label_3.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.right_top_label_3.setPixmap(QPixmap("../images/空.png"))
            self.right_top_label_3.setScaledContents(True)  # 让图片自适应label大小