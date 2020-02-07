from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import sys
import qtawesome
from NN_multiplication_table import NN_Table



class logindialog(QWidget):
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

    def __init__(self):
        super().__init__()
        self.setWindowTitle('首页')
        self.resize(1200, 900)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("../images/Natsume.ico"))  # 设置窗口图标
        self.setWindowTitle("猫咪老师课堂")  # 设置窗口名

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 100, 300, 780))
        self.verticalLayoutWidget.setObjectName("ButtonWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("ButtonLayout")

        self.pushButton_1 = QtWidgets.QPushButton("九九乘法表",self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("HomeButton")
        self.pushButton_1.setIcon(QIcon("../images/算法.png"))
        self.pushButton_1.setFixedSize(300,40)
        self.verticalLayout.addWidget(self.pushButton_1)

        self.pushButton_2 = QtWidgets.QPushButton("随机练习",self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("HomeButton")
        self.pushButton_2.setIcon(QIcon("../images/算法1.png"))
        self.pushButton_2.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton("算术考试",self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("HomeButton")
        self.pushButton_3.setIcon(QIcon("../images/考试.png"))
        self.pushButton_3.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'),"反馈建议",self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("HomeButton")
        self.pushButton_4.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_4)


        self.pushButton_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'),"联系我们",self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("HomeButton")
        self.pushButton_5.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'),"遇到问题",self.verticalLayoutWidget)
        self.pushButton_6.setObjectName("HomeButton")
        self.pushButton_6.setFixedSize(300, 40)
        self.verticalLayout.addWidget(self.pushButton_6)

        self.frame.setStyleSheet('''
        QWidget#Fram{
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
        self.frame.setVisible(True)

        self.Widget1 = NN_Table(self)
        # self.frame1 = QWidget(self)
        # self.frame1.setObjectName("Fram1")
        # self.verticalLayout1 = QVBoxLayout(self.frame1)
        # self.pushButton_quit_1 = QPushButton(self.frame1)
        # self.pushButton_quit_1.setText("回到主页面1")
        # self.verticalLayout1.addWidget(self.pushButton_quit_1)
        self.Widget1.frame.setVisible(False)


        self.frame2 = QWidget(self)
        self.verticalLayout2 = QVBoxLayout(self.frame2)
        self.pushButton_quit_2 = QPushButton(self.frame2)
        self.pushButton_quit_2.setText("回到主页面2")
        self.verticalLayout2.addWidget(self.pushButton_quit_2)
        self.frame2.setVisible(False)

        self.frame3 = QWidget(self)
        self.verticalLayout3 = QVBoxLayout(self.frame3)
        self.pushButton_quit_3 = QPushButton()
        self.pushButton_quit_3.setText("回到主页面3")
        self.verticalLayout3.addWidget(self.pushButton_quit_3)
        self.frame3.setVisible(False)

        self.pushButton_1.clicked.connect(self.on_pushButton_enter_clicked_1)
        self.pushButton_2.clicked.connect(self.on_pushButton_enter_clicked_2)
        self.pushButton_3.clicked.connect(self.on_pushButton_enter_clicked_3)
        self.Widget1.right_button_2.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit_2.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit_3.clicked.connect(self.on_pushButton_enter_clicked)

    def on_pushButton_enter_clicked_1(self):
        self.Widget1.frame.setVisible(True)
        self.Widget1.NN_Start()
        self.frame2.setVisible(False)
        self.frame3.setVisible(False)
        self.frame.setVisible(False)

    def on_pushButton_enter_clicked_2(self):
        self.Widget1.frame.setVisible(False)
        self.frame2.setVisible(True)
        self.frame3.setVisible(False)
        self.frame.setVisible(False)

    def on_pushButton_enter_clicked_3(self):
        self.Widget1.frame.setVisible(False)
        self.frame2.setVisible(False)
        self.frame3.setVisible(True)
        self.frame.setVisible(False)

    def on_pushButton_enter_clicked(self):
        self.Widget1.frame.setVisible(False)
        self.frame2.setVisible(False)
        self.frame3.setVisible(False)
        self.frame.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog()
    dialog.show()
    sys.exit(app.exec_())