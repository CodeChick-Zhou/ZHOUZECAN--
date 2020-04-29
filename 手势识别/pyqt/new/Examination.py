from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import copy
import random
import pygame
import time
from finger_train import *
from MusicThread import MusicSingleton
from VideoWorkThread import VideoSingleton
from Table import *
import GetFileName as File

NExamMutx = QMutex()
QmutVideo = QMutex()

# 正常考试停止信号
NExamStopFlag = False

# 手势识别次数
VideoTime = 2

# 考试时间
Nsec = 180
Asec = 180
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

# 手势识别考试定时器
class VDTimeVideoThread(QThread):

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
        print("********发送信号*********")
        self.workthread.emit()

        # print("********发送信号*********")

    def run(self):
        QmutVideo.lock()        # 加锁防止出现两个线程
        print("VDTimeVideoThread start run")
        global Nsec,Asec,QLineEditCount
        self.count = QLineEditCount


        while self.count:
            while True:
                if self.VideoStopFlag:
                    self.SignalButton.emit()
                    QmutVideo.unlock()
                    return

                self.sleep(1)  # 休眠1秒

                if self.VideoStopFlag:
                    self.SignalButton.emit()
                    QmutVideo.unlock()
                    return

                if Nsec == 0:
                    self.EndTime()
                    break

                self.timer.emit()  # 发送timer信号

            Nsec = Asec
            self.count -= 1
            print("self.count",self.count)

        print("VDTimeVideoThread end")
        VideoThreadEnd = True
        QmutVideo.unlock()

# 用于纠正错误的手势识别定时器
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
        print("********发送信号*********")
        self.workthread.emit()

        # print("********发送信号*********")

    def run(self):
        QmutVideo.lock()        # 加锁防止出现两个线程
        print("TimeVideoThread start run")
        global Nsec,Asec,QLineEditCount
        self.count = QLineEditCount

        while self.count:
            print("TimeVideoThread QLineEditCount")
            while True:
                print("TimeVideoThread Nsec", Nsec)
                if self.VideoStopFlag:
                    print("TimeVideoThread self.SignalButton.emit()")
                    self.SignalButton.emit()
                    QmutVideo.unlock()
                    return

                self.sleep(1)  # 休眠1秒
                print("TimeVideoThread sleep")

                if self.VideoStopFlag:
                    print("TimeVideoThread self.SignalButton.emit()")
                    self.SignalButton.emit()
                    QmutVideo.unlock()
                    return

                if Nsec == 0:
                    print("TimeVideoThread end")
                    self.EndTime()
                    break
                self.timer.emit()  # 发送timer信号
                print(" self.timer.emit()")

            # print("TimeVideoThread self.VideoStopFlag ", self.VideoStopFlag)
            # print("TimeVideoThread 结束 ",Rsec)
            # print("QLineEditCount ", QLineEditCount)
            Nsec = Asec
            self.count -= 1

        print("TimeVideoThread end")
        VideoThreadEnd = True
        QmutVideo.unlock()

# 定时三秒的定时器，平滑
class TimeVideoSleepThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()
    StopFlag = False
    Runstate = False

    def RunState(self):
        return self.Runstate

    def SetStopFlag(self,state):
        self.StopFlag = state

    def initFlag(self):
        self.Runstate = True
        self.StopFlag = False

    def run(self):
        QmutVideo.lock()
        global Nsec
        self.sleeptime = Nsec
        while True:

            self.sleep(1)
            print("self.sleeptime:",self.sleeptime)

            if self.StopFlag:
                self.Runstate = False
                break

            if self.sleeptime == 0:
                print("self.end.emit()")
                self.end.emit()
                break

            self.timer.emit()

            self.sleeptime -= 1

        self.Runstate = False
        print("TimeVideoSleepThread end")
        QmutVideo.unlock()

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
        # 为了获得坐标，传入父对象
        self.curparents = parents

        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(self.curparents.width(), self.curparents.height())
        # self.frame.setFixedSize(1200, 900)

        self.ButtonFlag = True
        self.init_frame(parents)

        self.frame1 = QWidget(parents)
        self.frame1.setObjectName("Frame1")
        self.frame1.resize(1200, 900)
        self.frame1.setFixedSize(self.curparents.width(), self.curparents.height())
        self.init_frame1(parents)

        self.frame2 = QWidget(parents)
        self.frame2.setObjectName("Frame2")
        self.frame2.resize(1200, 900)
        self.frame2.setFixedSize(self.curparents.width(), self.curparents.height())
        self.init_frame2(parents)

        self.frame.setVisible(False)
        self.frame1.setVisible(False)
        self.frame2.setVisible(False)

    # 改变背景
    def changebackimage(self):
        self.frame1.setStyleSheet('''
            QWidget#Frame1{
                border-image:url('''+File.path[File.curpathindex-1]+''');
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-right:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')

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
                border-image:url('''+File.path[File.curpathindex-1]+''');
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-right:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')

    # 显示对话框
    def ShowSubmitDialog(self):
        self.SubmitDialog = QDialog()

        self.SubmitDialog.resize(420,120)
        self.SubmitDialog.setFixedSize(420,120)

        self.SubmitEdit = QLineEdit(self.SubmitDialog)
        self.SubmitEdit.setReadOnly(True)
        self.SubmitEdit.resize(420,60)
        self.SubmitEdit.setFixedSize(420, 60)

        self.SubmitEdit.setStyleSheet("color:white;background:transparent;border-width:0;border-style:outset;font:25px")
        self.SubmitEdit.setAlignment(Qt.AlignCenter)
        self.SubmitEdit.setText(self.tip)

        self.SubmitHLayout = QtWidgets.QWidget(self.SubmitDialog)
        # self.HLayout.setGeometry(QtCore.QRect(0, 0, 300, 50))
        self.Submitbutton1 = QPushButton('确定',self.SubmitHLayout)
        self.Submitbutton1.setObjectName("DialogButton")
        self.Submitbutton2 = QPushButton('取消', self.SubmitHLayout)
        self.Submitbutton2.setObjectName("DialogButton")

        self.Submitbutton1.clicked.connect(self.SubmitDialog.close)
        self.Submitbutton1.clicked.connect(self.SleepGetScore)
        self.Submitbutton2.clicked.connect(self.SubmitDialog.close)

        self.SubmitDialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.SubmitDialog.setWindowOpacity(1)  # 设置窗口透明度
        # self.SubmitDialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.Submitbutton1.setFixedSize(100,30)
        self.Submitbutton2.setFixedSize(100,30)

        self.Submitbutton1.move(100, 80)
        self.Submitbutton2.move(200, 80)

        self.SubmitDialog.setObjectName("ExDialog")

        size1 = self.frame.geometry()
        size2 = self.SubmitDialog.geometry()
        self.SubmitDialog.move( self.curparents.x()+(size1.width()-size2.width())/2,
                            self.curparents.y()+(size1.height()-size2.height())/2)


        self.SubmitDialog.setStyleSheet('''
        QDialog{
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
        ''')

        self.SubmitHLayout.setStyleSheet('''
            QPushButton{border:none;color:white;font-size:25px}
            QPushButton:hover{
                    border-left:4px solid white;
                    font-size:28px;
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


    # 显示设置对话框
    def ShowDialog(self):
        self.Exdialog = QDialog()

        self.Exdialog.resize(420, 300)
        self.Exdialog.setFixedSize(420, 300)

        self.ExdialogWidget = QWidget(self.Exdialog)
        self.ExdialogWidget.resize(420, 300)
        self.ExdialogWidget.setFixedSize(420, 300)
        self.ExdialogWidget.setObjectName("dialog")

        self.label1 = QLabel(self.ExdialogWidget)
        self.label1.setText("时间设置")
        self.label1.setObjectName('label1')
        self.label1.setGeometry(QtCore.QRect(20, 40, 100, 80))

        self.label2 = QLabel(self.ExdialogWidget)
        self.label2.setObjectName('label1')
        self.label2.setText("题目数量")
        self.label2.setGeometry(QtCore.QRect(20, 110, 100, 80))

        self.ExdialogWidget.setStyleSheet("QLabel#label1{font-size:20px}")

        self.label1_button_left = QPushButton(self.ExdialogWidget)
        self.label1_button_right = QPushButton(self.ExdialogWidget)
        self.label1_button_left.setObjectName('btn1')
        self.label1_button_right.setObjectName('btn2')

        self.label1_button_left.setGeometry(QtCore.QRect(130, 50, 50, 50))
        self.label1_button_right.setGeometry(QtCore.QRect(300, 50, 50, 50))
        self.label1_button_left.clicked.connect(self.time_reduce)
        self.label1_button_right.clicked.connect(self.time_add)

        self.label2_button_left = QPushButton(self.ExdialogWidget)
        self.label2_button_right = QPushButton(self.ExdialogWidget)
        self.label2_button_left.setObjectName('btn1')
        self.label2_button_right.setObjectName('btn2')

        self.label2_button_left.setGeometry(QtCore.QRect(130, 120, 50, 50))
        self.label2_button_right.setGeometry(QtCore.QRect(300, 120, 50, 50))
        self.label2_button_left.clicked.connect(self.Number_reduce)
        self.label2_button_right.clicked.connect(self.Number_add)

        self.label1_LineEdit = QLineEdit(self.ExdialogWidget)
        self.label1_LineEdit.setGeometry(QtCore.QRect(190, 60, 100, 40))
        self.label1_LineEdit.setText(str(self.Timing))
        self.label1_LineEdit.setAlignment(Qt.AlignCenter)
        self.label1_LineEdit.setReadOnly(True)

        self.label2_LineEdit = QLineEdit(self.ExdialogWidget)
        self.label2_LineEdit.setGeometry(QtCore.QRect(190, 130, 100, 40))
        self.label2_LineEdit.setText(str(self.NumberQuestions))
        self.label2_LineEdit.setAlignment(Qt.AlignCenter)
        self.label2_LineEdit.setReadOnly(True)

        self.sbutton = QPushButton(self.ExdialogWidget)
        self.sbutton.setText("确定")
        self.sbutton.clicked.connect(self.Exdialog.close)
        self.sbutton.setGeometry(QtCore.QRect(280, 230, 100, 40))
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

        size1 = self.frame.geometry()       # 获取位置和尺寸
        size2 = self.Exdialog.geometry()
        # 计算居中的位置
        self.Exdialog.move( self.curparents.x()+(size1.width()-size2.width())/2,
                            self.curparents.y()+(size1.height()-size2.height())/2)

        self.Exdialog.exec()

    # 减少时间
    def time_reduce(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 30:
            return
        else:
            self.Timing -= 10
            self.label1_LineEdit.setText(str(self.Timing))

    # 增加时间
    def time_add(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 300:
            return
        else:
            self.Timing += 10
            self.label1_LineEdit.setText(str(self.Timing))
        return

    # 题目数量减少
    def Number_reduce(self):
        self.NumberQuestions = int(self.label2_LineEdit.text())
        if self.NumberQuestions == 10:
            return
        else:
            self.NumberQuestions -= 10
            self.label2_LineEdit.setText(str(self.NumberQuestions))

    # 题目数量增多
    def Number_add(self):
        self.NumberQuestions = int(self.label2_LineEdit.text())
        if self.NumberQuestions == 30:
            return
        else:
            self.NumberQuestions += 10
            self.label2_LineEdit.setText(str(self.NumberQuestions))

    # 获得手势识别的值，用于修改答案
    def GetTimeVideoResult(self,result):

        # 语音提醒
        MusicSingleton.start()

        self.NEQuestionCur[self.QuestionIndex][self.GAnswerIndex[0]] = result
        if self.GAnswerIndex[0] == 0:
            self.ChangeNumberImage(self.right_Number_LineEdit_1,result)
        elif self.GAnswerIndex[0] == 1:
            self.ChangeNumberImage(self.right_Number_LineEdit_2,result)
        elif self.GAnswerIndex[0] == 2:
            self.ChangeNumberImage(self.right_Number_LineEdit_3,result)
        elif self.GAnswerIndex[0] == 3:
            self.ChangeNumberImage(self.right_Number_LineEdit_4,result)

        del self.GAnswerIndex[0]
        del self.GAnswer[0]
        length = len(self.GAnswer)

        self.show_Arrow()
        if length==1:
            self.right_Number_LineEdit_6.setText("请对着摄像头的框框摆出第二个酷酷的手势"+str(self.GAnswer[0]))
            # del self.GAnswer[0]
        elif length==0:
            if self.IsTrue():
                QmutVideo.lock()
                self.right_button_1.setEnabled(True)
                self.right_button_2.setEnabled(False)
                self.right_button_3.setEnabled(True)
                self.right_button_5.setEnabled(True)
                self.right_Number_LineEdit_1.setReadOnly(True)
                self.right_Number_LineEdit_2.setReadOnly(True)
                self.right_Number_LineEdit_3.setReadOnly(True)
                self.right_Number_LineEdit_4.setReadOnly(True)
                self.right_Number_LineEdit_5.setText("回答正确，答案如下")
                self.right_Number_LineEdit_6.setText("")
                self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小


                VideoSingleton.SetShowFlag(False)
                QmutVideo.unlock()
                return
            else:
                QmutVideo.lock()
                global QLineEditCount,VideoTime
                if VideoTime == 1:
                    self.right_Number_LineEdit_5.setText("手势识别多次输入错误，请检查下手势的正确性以及周围环境")
                    self.right_Number_LineEdit_6.setText("正确答案如下")
                    self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
                    self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小


                    self.GetAnswer()
                    self.gifnoshow()
                    # self.Arrow_indication(0, False)
                    # self.Arrow_indication(1, False)
                    # self.Arrow_indication(2, False)
                    # self.Arrow_indication(3, False)

                    for i in range(0,len(self.GAnswerIndex)):
                        if self.GAnswerIndex[i] == 0:
                            self.ChangeNumberImage(self.right_Number_LineEdit_1, self.GAnswer[i])
                            self.NEQuestionCur[self.QuestionIndex][0] = self.GAnswer[i]
                        elif self.GAnswerIndex[i] == 1:
                            self.ChangeNumberImage(self.right_Number_LineEdit_2, self.GAnswer[i])
                            self.NEQuestionCur[self.QuestionIndex][1] = self.GAnswer[i]
                        elif self.GAnswerIndex[i] == 2:
                            self.ChangeNumberImage(self.right_Number_LineEdit_3, self.GAnswer[i])
                            self.NEQuestionCur[self.QuestionIndex][2] = self.GAnswer[i]
                        elif self.GAnswerIndex[i] == 3:
                            self.ChangeNumberImage(self.right_Number_LineEdit_4, self.GAnswer[i])
                            self.NEQuestionCur[self.QuestionIndex][3] = self.GAnswer[i]

                    # 重新初始化次数
                    VideoTime = 2

                    self.right_button_1.setEnabled(True)
                    self.right_button_2.setEnabled(False)
                    self.right_button_3.setEnabled(True)
                    self.right_button_5.setEnabled(True)

                    VideoSingleton.SetShowFlag(False)

                    QmutVideo.unlock()
                    return


                QLineEditCount = 0

                for i in range(0, len(self.NEStatus[self.QuestionIndex])):
                    if self.NEStatus[self.QuestionIndex][i]:
                        QLineEditCount += 1

                self.GetAnswer()
                self.show_Arrow()

                self.right_Number_LineEdit_5.setText("手势识别输入错误，请检查自己的手势，再次摆出手势")
                self.right_Number_LineEdit_6.setText("请对着摄像头的框框摆出酷酷的手势" + str(self.GAnswer[0]))
                # del self.GAnswer[0]

                VideoTime -= 1

                self.timevideothread.start()
                QmutVideo.unlock()

        return

    def VideoButtonConnect(self):
        return

    # 手势识别三秒之后下一题
    def VDend(self):

        QmutVideo.lock()
        QmutVideo.unlock()

        if self.timevideosleepthread.StopFlag:
            return

        global QLineEditCount,Nsec,Asec

        print("self.QuestionIndex",self.QuestionIndex)
        print("self.NumberQuestions",self.NumberQuestions)

        if self.QuestionIndex == self.NumberQuestions-1:
            print("VDend() self.QuestionIndex",self.QuestionIndex)

            if hasattr(self, "SubmitDialog"):
                if self.SubmitDialog.isActiveWindow():
                    self.SubmitDialog.close()


            print("self.SubmitDialog.close()")
            self.GetScore()
            return

        self.QuestionIndex += 1
        print("self.QuestionIndex",self.QuestionIndex)
        print("self.NumberQuestions",self.NumberQuestions)
        self.GetAnswer()
        self.VDcount = len(self.GAnswer)
        QLineEditCount = len(self.GAnswer)
        Nsec = int(self.Timing/self.NumberQuestions)
        Asec = int(self.Timing/self.NumberQuestions)
        self.ChangeTime()

        self.right_Number_LineEdit_5.setText("请根据题目，摆出相应的手势,使得公式相等")
        self.right_Number_LineEdit_6.setText("")

        # 显示题目
        self.VdShowExam()

        # 显示箭头
        self.show_Arrow()
        self.VDtimevideothread.start()
        # QmutVideo.unlock()

    # 手势识别调用的函数
    def VDGetTimeVideoResult(self,result):

        if self.VDtimevideothread.VideoStopFlag:
            return

        # 语音提醒
        MusicSingleton.start()

        print("VDGetTimeVideoResult() start")
        self.NEQuestionCur[self.QuestionIndex][self.GAnswerIndex[0]] = result
        if self.GAnswerIndex[0] == 0:
            self.ChangeNumberImage(self.right_Number_LineEdit_1,result)
        elif self.GAnswerIndex[0] == 1:
            self.ChangeNumberImage(self.right_Number_LineEdit_2,result)
        elif self.GAnswerIndex[0] == 2:
            self.ChangeNumberImage(self.right_Number_LineEdit_3,result)
        elif self.GAnswerIndex[0] == 3:
            self.ChangeNumberImage(self.right_Number_LineEdit_4,result)

        del self.GAnswerIndex[0]

        self.VDcount -= 1

        self.show_Arrow()
        if self.VDcount == 0:
            global Nsec
            if self.QuestionIndex == self.NumberQuestions-1:
                print("手势识别输入完毕，正在计算分数")
                self.right_Number_LineEdit_5.setText("手势识别输入完毕，正在计算分数")
                self.right_Number_LineEdit_6.setText("")
                Nsec = 3 # 3秒之后进入下一题
                self.ChangeTime()
                self.right_button_2.setEnabled(False)
                self.timevideosleepthread.initFlag()
                self.timevideosleepthread.start()
            else:
                self.IsTrue()
                self.right_Number_LineEdit_5.setText("手势识别输入完毕，即将进入下一题")
                print("手势识别输入完毕，即将进入下一题")
                self.right_Number_LineEdit_6.setText("")
                Nsec = 3 # 3秒之后进入下一题
                self.ChangeTime()
                print("self.ChangeTime()")
                self.timevideosleepthread.initFlag()
                self.timevideosleepthread.start()
        else:
            self.right_Number_LineEdit_5.setText("请根据题目，摆出相应的手势,使得公式相等")
            self.right_Number_LineEdit_6.setText("请输入第二个框")

        return

    # 手势识别模式
    FirstVDExam = True
    FirstErrorVideo = True
    def VideoExam(self):
        self.changebackimage()

        self.VDstart = True
        self.NDstart = False

        self.frame.setVisible(False)
        self.frame2.setVisible(False)
        self.frame1.setVisible(True)


        self.right_button_1.setHidden(True)
        self.right_button_2.setHidden(False)
        self.right_button_3.setHidden(True)
        self.right_button_4.setHidden(True)
        self.right_button_5.setHidden(True)

        self.right_button_2.setEnabled(True)

        global NExamStopFlag,Nsec,QLineEditCount,Asec
        NExamStopFlag = False
        print("self.Timing:",self.Timing)
        print("self.NumberQuestions:", self.NumberQuestions)
        Nsec = int(self.Timing/self.NumberQuestions)
        Asec = int(self.Timing/self.NumberQuestions)
        self.ChangeTime()

        # 非观察模式
        self.ViewFlag = False
        print("self.ViewFlag:",self.ViewFlag)

        if self.FirstErrorVideo:
            self.timevideothread = TimeVideoThread()
            self.timevideothread.timer.connect(self.countTime)
            self.timevideothread.workthread.connect(VideoSingleton.work)
            self.timevideothread.SignalButton.connect(self.VideoButtonConnect)

            self.FirstErrorVideo = False

        if self.FirstVDExam:

            self.timevideosleepthread = TimeVideoSleepThread()
            self.timevideosleepthread.timer.connect(self.countTime)
            self.timevideosleepthread.end.connect(self.VDend)

            self.VDtimevideothread = VDTimeVideoThread()
            self.VDtimevideothread.timer.connect(self.countTime)
            self.VDtimevideothread.workthread.connect(VideoSingleton.work)
            self.VDtimevideothread.SignalButton.connect(self.VideoButtonConnect)

            self.FirstVDExam = False

        self.VDtimevideothread.SetVideoSingleton(False)
        # 设置手势识别触发函数
        VideoSingleton.timer.connect(self.VDGetTimeVideoResult)

        # 获得题目
        self.ExamQuestion()

        # 当前题目下标
        self.QuestionIndex = 0

        # 显示题目
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
        self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        self.VdShowExam()

        self.GetAnswer()
        self.VDcount = len(self.GAnswer)


        QLineEditCount = len(self.GAnswer)

        print("self.VDcount",self.VDcount,"QLineEditCount",QLineEditCount)

        self.right_Number_LineEdit_5.setText("请根据题目，摆出相应的手势,使得公式相等")
        self.right_Number_LineEdit_6.setText("")

        VideoSingleton.SetShowFlag(True)

        # 显示箭头
        self.show_Arrow()

        self.VDtimevideothread.start()
        print("self.VDtimevideothread.start()")

    # 开始正常开始
    FirstNExam = True
    # 标志是手势识别还是正常模式
    NDstart = False
    VDstart = False
    def NormalExam(self):
        self.changebackimage()

        self.VDstart = False
        self.NDstart = True

        self.frame.setVisible(False)
        self.frame2.setVisible(False)
        self.frame1.setVisible(True)

        self.right_button_1.setHidden(False)
        self.right_button_2.setHidden(False)
        self.right_button_3.setHidden(False)
        self.right_button_4.setHidden(True)
        self.right_button_5.setHidden(True)

        self.right_button_1.setEnabled(True)
        self.right_button_2.setEnabled(True)
        self.right_button_3.setEnabled(True)
        self.right_button_5.setEnabled(False)

        # 设置线程停止标志
        global NExamStopFlag,Nsec
        NExamStopFlag = False
        print("self.Timing:",self.Timing)
        Nsec = self.Timing
        self.ChangeTime()

        # 非观察模式
        self.ViewFlag = False

        if self.FirstErrorVideo:
            self.timevideothread = TimeVideoThread()
            self.timevideothread.timer.connect(self.countTime)
            self.timevideothread.workthread.connect(VideoSingleton.work)
            self.timevideothread.SignalButton.connect(self.VideoButtonConnect)

            self.FirstErrorVideo = False

        if self.FirstNExam:
            self.NEtimeworkthread = NormalExamTimeWorkThread()
            self.NEtimeworkthread.timer.connect(self.countTime)
            self.NEtimeworkthread.end.connect(self.GetScore)
            self.NEtimeworkthread.SignalButton.connect(self.VideoButtonConnect)


            self.FirstNExam = False

        self.timevideothread.SetVideoSingleton(False)

        # 设置手势识别触发函数
        VideoSingleton.timer.connect(self.GetTimeVideoResult)

        # 获得题目
        self.ExamQuestion()

        # 当前题目下标
        self.QuestionIndex = 0

        # 显示题目
        self.right_bottom_label_1.setPixmap(QPixmap("../images/空.png"))
        self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
        self.right_Number_LineEdit_5.setText("请根据题目，在框中输入正确的数字,使得公式相等")
        self.right_Number_LineEdit_6.setText("")
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
        # self.right_Number_LineEdit_5.setStyleSheet("color:white;font:32px;background:transparent;border-width:0;border-style:outset")
        self.right_Number_LineEdit_6.setGeometry(QtCore.QRect(250, 330, 650, 40))
        self.right_Number_LineEdit_6.setAlignment(Qt.AlignCenter)
        # self.right_Number_LineEdit_6.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;border-style:outset")
        self.SetReadOnly(self.right_Number_LineEdit_5,True)
        self.SetReadOnly(self.right_Number_LineEdit_6,True)

        self.right_LineEdit_label_1 = QLabel(self.frame1)
        self.right_LineEdit_label_2 = QLabel(self.frame1)
        self.right_LineEdit_label_3 = QLabel(self.frame1)
        self.right_LineEdit_label_4 = QLabel(self.frame1)
        self.right_LineEdit_label_1.setGeometry(QtCore.QRect(125, 600, 100, 100))
        self.right_LineEdit_label_2.setGeometry(QtCore.QRect(425, 600, 100, 100))
        self.right_LineEdit_label_3.setGeometry(QtCore.QRect(725, 600, 100, 100))
        self.right_LineEdit_label_4.setGeometry(QtCore.QRect(865, 600, 100, 100))

        # self.right_LineEdit_label_1.setPixmap(QPixmap("../images/箭头2.png"))
        # self.right_LineEdit_label_1.setScaledContents(True)  # 让图片自适应label大小
        # self.right_LineEdit_label_1.setPixmap(QPixmap("../images/箭头2.png"))
        # self.right_LineEdit_label_1.setScaledContents(True)  # 让图片自适应label大小
        # self.right_LineEdit_label_2.setPixmap(QPixmap("../images/箭头2.png"))
        # self.right_LineEdit_label_2.setScaledContents(True)  # 让图片自适应label大小
        # self.right_LineEdit_label_3.setPixmap(QPixmap("../images/箭头2.png"))
        # self.right_LineEdit_label_3.setScaledContents(True)  # 让图片自适应label大小
        # self.right_LineEdit_label_4.setPixmap(QPixmap("../images/箭头2.png"))
        # self.right_LineEdit_label_4.setScaledContents(True)  # 让图片自适应label大小
        # self.right_LineEdit_label_4.setPixmap(QPixmap(""))
        # self.right_LineEdit_label_4.setScaledContents(True)  # 让图片自适应label大小



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
        self.right_bottom_LineEdit = QLabel(self.frame1)


        self.right_top_time_label.setGeometry(QtCore.QRect(500, 0, 130, 140))
        self.right_top_label_1.setGeometry(QtCore.QRect(440, 140, 80, 120))
        self.right_top_label_2.setGeometry(QtCore.QRect(510, 140, 80, 120))
        self.right_top_label_3.setGeometry(QtCore.QRect(585, 140, 80, 120))
        self.right_bottom_label_1.setGeometry(QtCore.QRect(490, 700, 168, 122))

        # 显示第几题
        self.right_bottom_LineEdit.setGeometry(QtCore.QRect(530,830, 200,60))
        self.right_bottom_LineEdit.setStyleSheet("color:black;font:32px;background:transparent;border-width:0;border-style:outset")


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

        self.right_button_4 = QtWidgets.QPushButton("修改答案", self.frame1)
        self.right_button_4.setGeometry(QtCore.QRect(910, 830, 100, 50))
        self.right_button_4.clicked.connect(self.ChangeAnswer)
        self.right_button_4.setHidden(True)
        self.right_button_4.setStyleSheet('''
            QPushButton{
                    background:#7bffbd;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
            QPushButton:hover{font-size:18px;background:#4affa5}
            ''')

        self.right_button_5 = QtWidgets.QPushButton("退出", self.frame1)
        self.right_button_5.clicked.connect(self.Back)
        self.right_button_5.setGeometry(QtCore.QRect(1050, 50, 100, 50))
        self.right_button_5.setStyleSheet('''
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 200, 300, 680))
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
        self.pushButton_2.clicked.connect(self.VideoExam)

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
                border-left:1px solid white;
                border-right:1px solid white;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
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
        self.frame2_QlineEdit1.setReadOnly(True)
        self.frame2_QlineEdit2.setReadOnly(True)

        self.frame2_button1.setGeometry(QtCore.QRect(190, 580, 320, 60))
        self.frame2_button2.setGeometry(QtCore.QRect(650, 585, 320, 60))
        self.frame2_button1.setStyleSheet("font:25px;")
        self.frame2_button2.setStyleSheet("font:25px;")
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


        self.label_star = QLabel(self.frame2)
        self.label_star.setGeometry(QtCore.QRect(20, 20, 40, 40))
        self.label_star.setPixmap(QPixmap("../images/star.png"))
        self.label_star.setScaledContents(True)  # 让图片自适应label大小

        self.LineEdit_star = QLineEdit(self.frame2)
        self.LineEdit_star.setGeometry(QtCore.QRect(70, 25, 80, 30))
        self.LineEdit_star.setReadOnly(True)
        self.LineEdit_star.setStyleSheet('''
                                        background: rgb(230,230,230);
                                        border-radius: 5px;
                                        border:1px solid rgb(180, 180, 180);
                                        font-size:25px
                                        ''')
        self.LineEdit_star.setText(str(File.curstars))
        self.LineEdit_star.setAlignment(Qt.AlignCenter)

    # ********************************方法****************************

    ViewFlag = False
    def ViewQuestion(self):
        VideoSingleton.timer.disconnect()
        VideoSingleton.timer.connect(self.GetTimeVideoResult)

        self.frame.setVisible(False)
        self.frame2.setVisible(False)
        self.frame1.setVisible(True)
        # ViewStart()
        self.ViewFlag =True
        self.QuestionIndex = 0
        self.right_button_2.setHidden(True)
        self.right_button_4.setHidden(False)
        self.right_button_5.setHidden(False)
        self.right_button_5.setEnabled(True)

        self.ShowExam()

        return

    # 返回
    def Back(self):
        self.frame2.setVisible(True)
        self.frame1.setVisible(False)
        self.frame.setVisible(False)

    # 返回主菜单
    def BackMain(self):
        VideoSingleton.timer.disconnect()
        self.frame2.setVisible(False)
        self.frame1.setVisible(False)
        self.frame.setVisible(True)

        self.right_button_5.setHidden(True)
        self.right_button_2.setHidden(False)

    # 改变计时时间
    def ChangeTime(self):
        global Nsec
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

    # 0-Easy 1-Medium 2-difficult
    Difficulty = 0
    # Easy-180  Medium-120   difficult-180
    Timing = 180
    # Number of questions
    NumberQuestions = 10

    # def SetDifficulty(self,result):
    #     global Nsec,Asec
    #     self.Difficulty = result
    #     print("Difficulty :",self.Difficulty)
    #     if self.Difficulty == 0 :
    #         self.Timing = 180
    #     elif self.Difficulty == 1:
    #         self.Timing = 120
    #     elif self.Difficulty == 2:
    #         self.Timing = 60
    #
    #     Nsec = self.Timing
    #     Asec = Nsec
    #
    #     self.ChangeTime()
    #
    #     # print("SetDifficulty() Nsec",Nsec)


    def GetScoreVDNE(self):
        # 判断最后一个题目的正确性
        if self.QuestionIndex == self.NumberQuestions - 1:
            self.IsTrue()

        # 正确的题目数
        self.correct = 0

        for i in range(0, len(self.NEAnswerCur)):
            if self.NEAnswerCur[i] == 1:
                self.correct += 1

        # 分数
        print("self.NEAnswerCur",self.NEAnswerCur)
        self.score = int(100 * self.correct / self.NumberQuestions)

        print("correct", self.correct, "score", self.score)

        self.tip1 = "本次一共有" + str(self.NumberQuestions) + "题，回答正确为" + str(self.correct) + "道"
        self.frame2_QlineEdit1.setText(self.tip1)
        # self.tip2 = "你的得分为:" + str(self.score) + "分"
        # self.frame2_QlineEdit2.setText(self.tip2)


        # 设置获得的星星
        staradd = 0
        if self.score < 60:
            staradd = 0
        elif self.score < 70:
            staradd = 1
        elif self.score < 80:
            staradd = 2
        elif self.score < 90:
            staradd = 3
        elif self.score < 100:
            staradd = 4
        elif self.score == 100:
            staradd = 5

        print("File.curstars", File.curstars)
        File.curstars += staradd
        print("File.curstars",File.curstars)

        self.tip2 = "你的得分为:" + str(self.score) + "分,获得了"+str(staradd)+"个⭐"
        self.frame2_QlineEdit2.setText(self.tip2)

        self.LineEdit_star.setText(str(File.curstars))
        File.writefilestar()

    # 获得分数
    def GetScore(self):
        # 消除箭头
        self.GAnswerIndex.clear()
        self.GAnswer.clear()
        self.gifnoshow()

        self.frame.setVisible(False)
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

        VideoSingleton.SetShowFlag(False)


        # 手势识别模式
        if self.VDstart:
            self.VDtimevideothread.SetVideoSingleton(True)
            self.right_button_2.setHidden(True)
            if self.timevideosleepthread.Runstate:
                self.timevideosleepthread.SetStopFlag(True)
            QmutVideo.lock()

            # 注意这里
            # self.timevideosleepthread.SetStopFlag(True)

            self.GetScoreVDNE()
            QmutVideo.unlock()
        # 正常模式
        else:
            global NExamStopFlag
            NExamStopFlag = True
            NExamMutx.lock()
            self.GetScoreVDNE()
            NExamMutx.unlock()

    def SleepGetScore(self):
        self.GetScore()


    # 提交试卷
    def SubmitExam(self):
        if self.NDstart:
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

        elif self.VDstart:
            self.tip = "还有题目没做完，是否要提交试卷"
            self.ShowSubmitDialog()

    # 计数器
    def countTime(self):
        global Nsec

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

        print("countTime")

    # 获得考试题目
    # 答案
    NEQuestion = []
    # 题目现状
    NEQuestionCur = []
    # 题目正确 0-false,1-true,2-no run
    NEAnswerCur = []
    # 编辑框状态
    NEStatus = []
    def ExamQuestion(self):
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
            i = random.randint(0,6)
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

    # 手势识别模式下显示
    def VdShowExam(self):
        self.SetReadOnly(self.right_Number_LineEdit_1, True)
        self.SetReadOnly(self.right_Number_LineEdit_2, True)
        self.SetReadOnly(self.right_Number_LineEdit_3, True)
        self.SetReadOnly(self.right_Number_LineEdit_4, True)

        for i in range(0, len(self.NEStatus[self.QuestionIndex])):
            print("VdShowExam i : ", i)
            if self.NEStatus[self.QuestionIndex][i] == True:
                if i == 0:
                    self.SetReadOnly(self.right_Number_LineEdit_1, False)
                    self.right_Number_LineEdit_1.setReadOnly(True)
                if i == 1:
                    self.SetReadOnly(self.right_Number_LineEdit_2, False)
                    self.right_Number_LineEdit_2.setReadOnly(True)
                if i == 2:
                    self.SetReadOnly(self.right_Number_LineEdit_3, False)
                    self.right_Number_LineEdit_3.setReadOnly(True)
                if i == 3:
                    self.SetReadOnly(self.right_Number_LineEdit_4, False)
                    self.right_Number_LineEdit_4.setReadOnly(True)

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

        self.ChangeNumberImage(self.right_Number_LineEdit_1, firstvalue)
        self.ChangeNumberImage(self.right_Number_LineEdit_2, secondvalue)

        if fourthvalue != -2:
            self.right_Number_LineEdit_4.setHidden(False)
        else:
            self.right_Number_LineEdit_4.setHidden(True)

        self.ChangeNumberImage(self.right_Number_LineEdit_3, thirdvalue)
        self.ChangeNumberImage(self.right_Number_LineEdit_4, fourthvalue)

        curstr = "第"+str(self.QuestionIndex+1)+"题"
        self.right_bottom_LineEdit.setText(curstr)
        print("VdShowExam() curstr",curstr)

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

        curstr = "第" + str(self.QuestionIndex + 1) + "题"
        self.right_bottom_LineEdit.setText(curstr)


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
        print("self.NEQuestionCur[self.QuestionIndex]",self.NEQuestionCur[self.QuestionIndex])
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
                if firstvalue + secondvalue == thirdvalue*10 + fourthvalue:
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
        if self.IsTrue():
            self.right_button_4.setHidden(True)
            self.right_Number_LineEdit_5.setText("回答正确")
            self.right_Number_LineEdit_6.setText("")
            self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            self.ShowQLineEdit()        # 显示题目

            # 设置编辑框有框框，方便查看填空
            for i in range(0, len(self.NEStatus[self.QuestionIndex])):
                print("i : ", i)
                if self.NEStatus[self.QuestionIndex][i] == True:
                    if i == 0:
                        self.right_Number_LineEdit_1.setReadOnly(True)
                    if i == 1:
                        self.right_Number_LineEdit_2.setReadOnly(True)
                    if i == 2:
                        self.right_Number_LineEdit_3.setReadOnly(True)
                    if i == 3:
                        self.right_Number_LineEdit_4.setReadOnly(True)


        else:
            self.right_button_4.setHidden(False)
            self.right_Number_LineEdit_5.setText("回答错误，请试着修改答案")
            self.right_Number_LineEdit_6.setText("")
            self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            self.ShowQLineEdit()    # 显示题目


        return

    # 修改答案
    AnswerStatus = []
    def ChangeAnswer(self):
        if self.IsTrue():
            self.right_Number_LineEdit_5.setText("恭喜你，回答正确")
            self.right_bottom_label_1.setPixmap(QPixmap("../images/对号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小
            self.right_Number_LineEdit_1.setReadOnly(True)
            self.right_Number_LineEdit_2.setReadOnly(True)
            self.right_Number_LineEdit_3.setReadOnly(True)
            self.right_Number_LineEdit_4.setReadOnly(True)

        else:
            for i in range(0, len(self.NEStatus[self.QuestionIndex])):
                print("i : ", i)
                if self.NEStatus[self.QuestionIndex][i] == True:
                    if i == 0:
                        self.right_Number_LineEdit_1.setReadOnly(True)
                    if i == 1:
                        self.right_Number_LineEdit_2.setReadOnly(True)
                    if i == 2:
                        self.right_Number_LineEdit_3.setReadOnly(True)
                    if i == 3:
                        self.right_Number_LineEdit_4.setReadOnly(True)

            cur = self.QuestionIndex
            if self.NEQuestion[self.QuestionIndex][3] == -2:
                value = self.NEQuestion[self.QuestionIndex][2]
            else:
                value = self.NEQuestion[self.QuestionIndex][2]*10+self.NEQuestion[self.QuestionIndex][3]
            curstr = str(self.NEQuestion[cur][0])+self.NEQuestion[cur][4]+str(self.NEQuestion[cur][1])+"="+str(value)

            print("str(self.NEQuestion[cur][0])",str(self.NEQuestion[cur][0]))
            print("str(self.NEQuestion[cur][1])", str(self.NEQuestion[cur][1]))
            print("str(self.NEQuestion[cur][2])", str(self.NEQuestion[cur][2]))
            print("str(self.NEQuestion[cur][3])", str(self.NEQuestion[cur][3]))
            print("str(self.NEQuestion[cur][4])", str(self.NEQuestion[cur][4]))
            print("curstr",curstr)
            self.right_Number_LineEdit_5.setText("回答错误，正确答案是"+curstr)
            self.right_bottom_label_1.setPixmap(QPixmap("../images/错号.png"))
            self.right_bottom_label_1.setScaledContents(True)  # 让图片自适应label大小

            self.AnswerStatus = copy.deepcopy(self.NEStatus[self.QuestionIndex])

            global QLineEditCount,Nsec,Asec,VideoTime
            Asec = 10
            Nsec = Asec
            self.ChangeTime()
            QLineEditCount = 0

            for i in range(0,len(self.NEStatus[self.QuestionIndex])):
                if self.NEStatus[self.QuestionIndex][i]:
                    QLineEditCount += 1


            self.GetAnswer()

            self.right_button_1.setEnabled(False)
            self.right_button_2.setEnabled(False)
            self.right_button_3.setEnabled(False)
            self.right_button_5.setEnabled(False)
            self.right_button_4.setHidden(True)
            self.right_Number_LineEdit_6.setText("请对着摄像头的框框摆出酷酷的手势"+str(self.GAnswer[0]))
            # del self.GAnswer[0]
            VideoSingleton.SetShowFlag(True)

            VideoTime = 2

            self.show_Arrow()

            self.timevideothread.start()
            return

    # 获得答案
    GAnswer=[]
    GAnswerIndex = []
    def GetAnswer(self):
        self.GAnswer = []
        self.GAnswerIndex = []
        for i in range(0,len(self.NEStatus[self.QuestionIndex])):
            if self.NEStatus[self.QuestionIndex][i]==True:
                self.GAnswer.append(self.NEQuestion[self.QuestionIndex][i])
                self.GAnswerIndex.append(i)

    # 设置编辑框只读，同时无框
    def SetReadOnly(self,right_Number_LineEdit,flag):
        if flag:
            right_Number_LineEdit.setReadOnly(True)
            right_Number_LineEdit.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;border-style:outset")
        else:
            right_Number_LineEdit.setReadOnly(False)
            right_Number_LineEdit.setStyleSheet("color:white;font:30px;background:transparent;border-width:0;")

    # 显示题目
    def ShowQLineEdit(self):
        print("ShowQLineEdit() start")

        self.SetReadOnly(self.right_Number_LineEdit_1, True)
        self.SetReadOnly(self.right_Number_LineEdit_2, True)
        self.SetReadOnly(self.right_Number_LineEdit_3, True)
        self.SetReadOnly(self.right_Number_LineEdit_4, True)


        for i in range(0, len(self.NEStatus[self.QuestionIndex])):
            print("i : ", i)
            if self.NEStatus[self.QuestionIndex][i] == True:
                if i == 0:
                    self.SetReadOnly(self.right_Number_LineEdit_1, False)
                if i == 1:
                    self.SetReadOnly(self.right_Number_LineEdit_2, False)
                if i == 2:
                    self.SetReadOnly(self.right_Number_LineEdit_3, False)
                if i == 3:
                    self.SetReadOnly(self.right_Number_LineEdit_4, False)

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



    # 显示箭头
    def show_Arrow(self):
        self.gifnoshow()

        if len(self.GAnswerIndex) >= 1:
            self.Arrow_indication(self.GAnswerIndex[0])

    # 设置箭头
    def Arrow_indication(self,index):
        if index == 0:
            self.Arrow_gif(self.right_LineEdit_label_1)
        elif index == 1:
            self.Arrow_gif(self.right_LineEdit_label_2)
        elif index == 2:
            self.Arrow_gif(self.right_LineEdit_label_3)
        elif index == 3:
            self.Arrow_gif(self.right_LineEdit_label_4)

    def Arrow_gif(self,right_LineEdit_label):
        self.gif = QMovie('../images/箭头动态.gif')
        self.gif.setScaledSize(QSize(self.right_LineEdit_label_1.width(), self.right_LineEdit_label_1.height()))
        right_LineEdit_label.setMovie(self.gif)
        self.gif.start()
        # self.gif.stateChanged.disconnect(lambda :self.gifshowAgain(self.gif,self.gif.NotRunning))
        self.gif.stateChanged.connect(lambda :self.gifshowAgain(self.gif))

    def gifnoshow(self):
        self.gif = QMovie('')
        self.right_LineEdit_label_1.setMovie(self.gif)
        self.right_LineEdit_label_2.setMovie(self.gif)
        self.right_LineEdit_label_3.setMovie(self.gif)
        self.right_LineEdit_label_4.setMovie(self.gif)

    def gifshowAgain(self,gif):
        state = gif.state()
        if state == gif.Running:
            return
        elif state == gif.Paused:
            return
        elif state == gif.NotRunning:
            gif.start()
        print("gifshowAgain start()")





