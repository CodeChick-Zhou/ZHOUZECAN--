# coding:utf-8
from finger_train import *
from video_test import *
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qtawesome
import picture as pic
import cv2
import msvcrt

NumberDict = {'1': "../images/number1.png", '2': "../images/number2.png", '3': "../images/number3.png",
              '4': "../images/number4.png", '5': "../images/number5.png", '6': "../images/number6.png",
              '7': "../images/number7.png", '8': "../images/number8.png", '9': "../images/number1.png",
              '0': "../images/number0.png"}

SymbolDict = {0: "../images/加号.png", 1: "../images/减号.png" , 2: "../images/乘号.png"}

# 正常大小无衬线字体
font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1
# ROI框的显示位置
x0 = 330
y0 = 40
# 录制的手势图片大小
width = 300
height = 300

# 前置摄像头判断的数值
VideoNumber = 0
count = 0

class VideoThread(QThread):
    timer = pyqtSignal()

    def ChangeNumberImageGui(self,gui,s):
        print("s:",s)
        global VideoNumber
        print("VideoNumber",VideoNumber)
        value = int(VideoNumber)
        print("value", value)
        gui.ChangeNumberImage(gui.right_Number_LineEdit_1, value)


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
        global VideoNumber
        cap = cv2.VideoCapture(0)
        global count
        while (True):
            # 读帧
            ret, frame = cap.read()
            # 图像翻转
            frame = cv2.flip(frame, 2)
            # 显示ROI区域  #调       用函数
            VideoNumber = self.Getbinary(frame, x0, y0, width, height, finger_model)

            count += 1
            if count%10 == 0:
                self.timer.emit()
            # 等待键盘输入
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            cv2.imshow("frame", frame)

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        finger_model = loadCNN()
        finger_model.load_weights("model/model_2019_11_20_best.hdf5")
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

    # 文本修改
    def textchanged(self,right_Number_LineEdit):
        text = right_Number_LineEdit.text()
        if text == "":
            return

        if not is_number(text):
            right_Number_LineEdit.setText("")
            return

        if int(text)>=0 & int(text)<=9:
            self.ChangeNumberImage(right_Number_LineEdit,int(text))


        print("before right_Number_LineEdit_1 text:",self.right_Number_LineEdit_1.text())
        right_Number_LineEdit.setText("")
        print("after right_Number_LineEdit_1 text:", self.right_Number_LineEdit_1.text())

    def ChangeNumberImage(self,right_Number_LineEdit,number):
        filename = "../images/number"+str(number)+".png"
        print("filename:",filename)
        pal = right_Number_LineEdit.palette()
        pal.setBrush(QPalette.Base,QBrush(QPixmap(filename).scaled(right_Number_LineEdit.size())))
        right_Number_LineEdit.setAutoFillBackground(True)
        right_Number_LineEdit.setPalette(pal)

    # 初始化页面右侧
    def init_right(self):
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格


        self.right_Number_LineEdit_1 = QLineEdit(self)
        self.right_Number_LineEdit_1.setObjectName('right_Number')
        self.right_Number_LineEdit_2 = QLineEdit(self)
        self.right_Number_LineEdit_2.setObjectName('right_Number')
        self.right_Number_LineEdit_3 = QLineEdit(self)
        self.right_Number_LineEdit_3.setObjectName('right_Number')
        self.right_Number_LineEdit_4 = QLineEdit(self)
        self.right_Number_LineEdit_4.setObjectName('right_Number')

        self.right_Number_LineEdit_1.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_2.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_3.setEchoMode(QLineEdit.NoEcho)
        self.right_Number_LineEdit_1.textChanged.connect(lambda :self.textchanged(self.right_Number_LineEdit_1))
        self.right_Number_LineEdit_2.textChanged.connect(lambda :self.textchanged(self.right_Number_LineEdit_2))
        self.right_Number_LineEdit_3.textChanged.connect(lambda :self.textchanged(self.right_Number_LineEdit_3))

        # self.right_Number_LineEdit_1.setStyleSheet("border:2px groove gray;padding:2px 4px")


        self.right_label1 = QLabel(self)
        self.right_label2 = QLabel(self)

        self.right_Number_LineEdit_1.setFixedSize(140,200)
        self.right_Number_LineEdit_2.setFixedSize(140,200)
        self.right_Number_LineEdit_3.setFixedSize(140,200)
        self.right_Number_LineEdit_4.setFixedSize(140,200)

        self.ChangeNumberImage(self.right_Number_LineEdit_1, 2)
        self.ChangeNumberImage(self.right_Number_LineEdit_2, 2)
        self.ChangeNumberImage(self.right_Number_LineEdit_3, 4)

        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(../images/number2.png")
        # self.right_Number_label1.setStyleSheet("background-image:url(../images/number2.png);")
        # self.right_Number_label2.setStyleSheet("background-image: url(../images/number2.png)}")
        # self.right_Number_label3.setStyleSheet("background-image: url(../images/number4.png)}")
        # self.right_Number_LineEdit_1.setStyleSheet("background-image:url(:../images/number2.png);\n""background-attachment:fixed;\n""background-repeat:none;\n""background-position:center")

        self.right_label1.setFixedSize(140,100)
        self.right_label1.setToolTip('这是一个图片标签')
        self.right_label1.setPixmap(QPixmap("../images/乘号.png"))
        self.right_label1.setScaledContents(True)  # 让图片自适应label大小

        self.right_label2.setFixedSize(140,100)
        self.right_label2.setToolTip('这是一个图片标签')
        self.right_label2.setPixmap(QPixmap("../images/等号.png"))
        self.right_label2.setScaledContents(True)  # 让图片自适应label大小2


        self.right_layout.addWidget(self.right_Number_LineEdit_1, 4, 0, 4, 3)
        self.right_layout.addWidget(self.right_label1, 5, 1, 2, 2)
        self.right_layout.addWidget(self.right_Number_LineEdit_2, 4, 2, 4, 3)
        self.right_layout.addWidget(self.right_label2, 5, 3, 2, 2)
        self.right_layout.addWidget(self.right_Number_LineEdit_3, 4, 4, 4, 3)
        self.right_layout.addWidget(self.right_Number_LineEdit_4, 4, 5, 4, 3)
        # self.right_Number_LineEdit_4.setHidden(True)


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

        self.setFixedSize(1280, 860)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.init_right()

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 12)  # 右侧部件在第0行第3列，占12行11列
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
                border-bottom:2px solid #bfe6ba;
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



def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()

    videothread = VideoThread()
    videothread.timer.connect(lambda :videothread.ChangeNumberImageGui(gui,count))
    videothread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()