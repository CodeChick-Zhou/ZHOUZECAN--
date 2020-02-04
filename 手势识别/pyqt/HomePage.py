'''

实现不规则窗口（异形窗口）

通过mask实现异形窗口

需要一张透明的png图，透明部分被扣出，形成一个非矩形的区域


移动和关闭不规则窗口
'''

import time
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qtawesome

# 主页面
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

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

    # 最小化和关闭按钮
    def init_CloseButton(self):
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_close.setFixedSize(30, 30)  # 设置关闭按钮的大小
        self.left_mini.setFixedSize(30, 30)  # 设置最小化按钮大小
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 1, 1, 1)

        self.left_mini.clicked.connect(self.showMinimized)
        self.left_close.clicked.connect(self.close)

    # 初始化页面右侧
    def init_right(self):
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                background:white;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-right:1px solid white;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')

    # 初始化页面左侧
    def init_ui(self):
        self.setWindowIcon(QIcon("../images/Natsume.ico"))  # 设置窗口图标
        self.setWindowTitle("猫咪老师课堂")  # 设置窗口名

        self.setFixedSize(1080, 760)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.init_right()

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占12行11列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.init_CloseButton()

        self.left_label_1 = QtWidgets.QPushButton("算术练习")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_2.setObjectName('left_label')

        # self.left_button_0 = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "首页")
        self.left_button_0 = QtWidgets.QPushButton("首页")
        self.left_button_0.setIcon(QIcon("../images/首页.png"))
        self.left_button_0.setObjectName('left_button0')
        self.left_button_1 = QtWidgets.QPushButton("九九乘法表")
        self.left_button_1.setIcon(QIcon("../images/算法.png", ))
        self.left_button_1.setObjectName('left_button1')
        self.left_button_2 = QtWidgets.QPushButton("随机练习")
        self.left_button_2.setObjectName('left_button1')
        self.left_button_2.setIcon(QIcon("../images/算法1.png"))
        self.left_button_3 = QtWidgets.QPushButton("算术考试")
        self.left_button_3.setObjectName('left_button1')
        self.left_button_3.setIcon(QIcon("../images/考试.png"))
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_4.setObjectName('left_button2')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_5.setObjectName('left_button2')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_6.setObjectName('left_button2')
        self.left_xxx = QtWidgets.QPushButton(" ")

        self.left_layout.addWidget(self.left_button_0, 1, 0, 1, 2)
        self.left_layout.addWidget(self.left_label_1, 2, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_1, 3, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_2, 4, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_3, 5, 0, 1, 2)
        self.left_layout.addWidget(self.left_label_2, 6, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_4, 7, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_5, 8, 0, 1, 2)
        self.left_layout.addWidget(self.left_button_6, 9, 0, 1, 2)

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid black;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button0{font-size:20px;}
            QPushButton#left_button0:hover{border-left:4px solid green;font-weight:700;font-size:24px;}
            QPushButton#left_button1:hover{border-left:4px solid red;font-weight:700;font-size:16px;}
            QPushButton#left_button2:hover{border-left:4px solid blue;font-weight:700;font-size:18px;}

            QWidget#left_widget{
                background:QLinearGradient(x1:1, y1:1, x2:0, y2:0, stop: 0 rgb(211,149,155)  , stop: 1 rgb(191,230,186));
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        # self.main_widget.setStyleSheet('''
        #     QWidget#main_widget{
        #         background:green;
        #     }
        # ''')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.main_layout.setSpacing(0)
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

# 展示首页动画
class AbnormityWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("异形窗口")
        self.pix = QBitmap('../images/mask2.png')
        self.resize(self.pix.size())
        self.setMask(self.pix)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.m_drag = True
    #
    #         self.m_DragPosition = event.globalPos() - self.pos()
    #         self.setCursor(QCursor(Qt.OpenHandCursor))
    #         print(event.globalPos())  #
    #         print(event.pos())
    #         print(self.pos())
    #     if event.button() == Qt.RightButton:
    #         self.close()
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     if Qt.LeftButton and self.m_drag:
    #         # 当左键移动窗体修改偏移值
    #         # QPoint
    #         # 实时计算窗口左上角坐标
    #         self.move(QMouseEvent.globalPos() - self.m_DragPosition)
    #
    #
    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.m_drag = False
    #     self.setCursor(QCursor(Qt.ArrowCursor))
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.pix.width(),self.pix.height(),QPixmap('../images/1.jpg'))

# 线程通知
class HomeWorkThread(QThread):
    timer = pyqtSignal()  # 5秒发送一次信号

    def run(self):
        self.sleep(5)
        self.timer.emit()

# 结束首页动画，展示主页面
def HomePage(window,main_window):
    window.close()
    main_window.show()

def main():
    app = QApplication(sys.argv)
    window = AbnormityWindow()
    main_window = MainUi()
    window.show()

    workthread = HomeWorkThread()

    workthread.timer.connect(lambda:HomePage(window,main_window))
    workthread.start()
    # timer = QTimer()
    # timer.timeout.connect(lambda:HomePage(form))
    # timer.start(2000)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
