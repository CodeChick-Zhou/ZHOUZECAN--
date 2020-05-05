
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import sys
import qtawesome
import time
from Random_practice import Random_Practice
from NN_multiplication_table import NN_Table
from Examination import Examination
from VideoWorkThread import VideoSingleton
from ContactUs import ContactUs
from Background import Background
from DayTrain import DayTrain
from MusicThread import MusicSingleton

class HomeWorkThread(QThread):
    timer = pyqtSignal()  # 5秒发送一次信号

    def run(self):
        self.sleep(5)
        self.timer.emit()

# 等待短暂时间使得其他定时器可以退出
class SleepThread(QThread):
    def __init__(self):
        super().__init__()


    timer = pyqtSignal()
    def run(self):
        time.sleep(0.8)
        self.timer.emit()

# 展示页面
class AbnormityWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵喵")
        self.pix = QBitmap('../images/mask2.png')
        self.resize(self.pix.size())
        self.setMask(self.pix)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.pix.width(),self.pix.height(),QPixmap('../images/1.jpg'))

class Main_ui(QWidget):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


    def initThread(self):
        self.Sleepthread = SleepThread()
        self.Sleepthread.timer.connect(self.ButtonConnect)

    def __init__(self):
        super().__init__()

        self.initThread()

        self.setWindowTitle('首页')
        self.resize(1200, 900)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("../images/Natsume.ico"))  # 设置窗口图标
        self.setWindowTitle("猫咪老师课堂")  # 设置窗口名

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.frame = QWidget(self)
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(self.width(), self.height())
        self.frame.setObjectName("Fram")

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
        self.pushButton_min.clicked.connect(self.showMinimized)
        self.pushButton_close.clicked.connect(self.close)


        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 200, 300, 680))
        self.verticalLayoutWidget.setObjectName("ButtonWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("ButtonLayout")

        self.pushButton_1 = QtWidgets.QPushButton("平日训练",self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("HomeButton")
        self.pushButton_1.setIcon(QIcon("../images/算法.png"))
        self.pushButton_1.setFixedSize(300,40)
        self.verticalLayout.addWidget(self.pushButton_1)

        self.pushButton_3 = QtWidgets.QPushButton("算术考试",self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("HomeButton")
        self.pushButton_3.setIcon(QIcon("../images/考试.png"))
        self.pushButton_3.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'),"星星商城",self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("HomeButton")
        self.pushButton_5.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton_4 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'),"联系我们",self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("HomeButton")
        self.pushButton_4.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.frame.setStyleSheet('''
        QWidget#Fram{
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
        self.frame.setVisible(True)

        self.Widget1 = DayTrain(self)
        self.Widget1.frame.setVisible(False)

        # self.Widget1 = NN_Table(self)
        # self.Widget1.frame.setVisible(False)
        #
        # self.Widget2 = Random_Practice(self)
        # self.Widget2.frame.setVisible(False)

        self.Widget3 = Examination(self)
        self.Widget3.frame.setVisible(False)
        self.Widget3.frame1.setVisible(False)

        self.Widget4 = ContactUs(self)
        self.Widget4.frame.setVisible(False)

        self.Widget5 = Background(self)
        self.Widget5.frame.setVisible(False)

        self.pushButton_1.clicked.connect(self.on_pushButton_enter_clicked_1)
        # self.pushButton_2.clicked.connect(self.on_pushButton_enter_clicked_2)
        self.pushButton_3.clicked.connect(self.on_pushButton_enter_clicked_3)
        self.pushButton_4.clicked.connect(self.on_pushButton_enter_clicked_4)
        self.pushButton_5.clicked.connect(self.on_pushButton_enter_clicked_5)
        # self.Widget1.right_button_2.clicked.connect(self.on_pushButton_enter_clicked_sleep)
        # self.Widget2.right_button_2.clicked.connect(self.on_pushButton_enter_clicked_sleep2)
        self.Widget1.pushButton_4.clicked.connect(self.on_pushButton_enter_clicked)
        self.Widget3.pushButton_4.clicked.connect(self.on_pushButton_enter_clicked)
        self.Widget4.pushButton_1.clicked.connect(self.on_pushButton_enter_clicked)
        self.Widget5.backbutton.clicked.connect(self.on_pushButton_enter_clicked)

        self.center()
        print("self.frame.x()",self.x())
        print("self.frame.y()",self.y())
        # self.pushButton_quit.clicked.connect(self.on_pushButton_enter_clicked)

        # VideoSingleton.start()

    def SetDifficulty(self,s):
        print(s)

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
        self.button1.clicked.connect(lambda :self.SetDifficulty(0))
        self.button2.clicked.connect(self.Exdialog.close)
        self.button2.clicked.connect(lambda: self.SetDifficulty(1))
        self.button3.clicked.connect(self.Exdialog.close)
        self.button3.clicked.connect(lambda: self.SetDifficulty(2))

        self.Exdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.Exdialog.setWindowOpacity(1)  # 设置窗口透明度
        self.Exdialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # screen = QDesktopWidget().screenGeometry()


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

    def on_pushButton_enter_clicked_1(self):
        self.Widget1.frame.setVisible(True)
        # self.Widget2.frame.setVisible(False)
        self.Widget3.frame.setVisible(False)
        self.Widget4.frame.setVisible(False)
        # self.Widget3.frame1.setVisible(False)
        self.frame.setVisible(False)
        self.Widget5.frame.setVisible(False)
        # self.Widget1.Start()

    def on_pushButton_enter_clicked_3(self):
        self.Widget1.frame.setVisible(False)
        # self.Widget2.frame.setVisible(False)
        self.Widget3.frame.setVisible(True)
        # self.Widget3.frame1.setVisible(False)
        self.Widget4.frame.setVisible(False)

        print("self.Widget3.frame.x()",self.Widget3.frame.frameGeometry().x())
        print("self.Widget3.frame.y()",self.Widget3.frame.frameGeometry().y())
        print("self.frame.x()",self.x())
        print("self.frame.y()",self.y())
        self.frame.setVisible(False)
        self.Widget5.frame.setVisible(False)

    def on_pushButton_enter_clicked_4(self):
        self.Widget1.frame.setVisible(False)
        # self.Widget2.frame.setVisible(False)
        self.Widget3.frame.setVisible(False)
        self.frame.setVisible(False)
        self.Widget4.frame.setVisible(True)
        self.Widget5.frame.setVisible(False)

    def on_pushButton_enter_clicked_5(self):
        self.Widget1.frame.setVisible(False)
        # self.Widget2.frame.setVisible(False)
        self.Widget3.frame.setVisible(False)
        self.frame.setVisible(False)
        self.Widget4.frame.setVisible(False)
        self.Widget5.frame.setVisible(True)
        self.Widget5.start()

    def on_pushButton_enter_clicked(self):
        self.Widget1.frame.setVisible(False)
        # self.Widget2.frame.setVisible(False)
        self.Widget3.frame.setVisible(False)
        self.Widget4.frame.setVisible(False)
        self.Widget5.frame.setVisible(False)
        self.frame.setVisible(True)

    def ButtonConnect(self):
        self.on_pushButton_enter_clicked()
        # self.Widget1.right_button_1.setEnabled(True)
        # self.Widget1.right_button_2.setEnabled(True)
        # self.Widget2.right_button_1.setEnabled(True)
        # self.Widget2.right_button_2.setEnabled(True)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


# 结束首页动画，展示主页面
def HomePage(window,main_window):
    window.close()
    main_window.show()

if __name__ == "__main__":
    print("start")
    app = QApplication(sys.argv)
    print("init QApplication,ui")
    window = Main_ui()
    AbWindow = AbnormityWindow()
    AbWindow.show()
    # window.show()

    # window.move(300,300)
    print("window.x()", window.x())
    print("window.y()", window.y())

    # 开始摄像头
    VideoSingleton.start()
    VideoSingleton.SetShowFlag(False)


    workthread = HomeWorkThread()
    workthread.timer.connect(lambda:HomePage(AbWindow,window))
    workthread.start()

    print("end while")
    sys.exit(app.exec_())