import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import time

# [] + [1] = [2][3]
if self.addRandom == 0:
    self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, -1)
# [1] + [] = [2][3]
elif self.addRandom == 1:
    self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, -1)
# [] + []  = [1][2]
elif self.addRandom == 2:
    self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, -1)
    self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, -1)
# [1] + [2] = [][]
elif self.addRandom == 3:
    self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, -1)
    self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, -1)

# [] - [1] = [2]
if self.minusRandom == 0:
    self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, -1)
# [1] - [] = [2]
elif self.minusRandom == 1:
    self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, -1)
# [] - [] = [2]
elif self.minusRandom == 2:
    self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, -1)
    self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, -1)
# [1] - [2] = []
elif self.minusRandom == 3:
    self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, -1)

# [1] + [2] = [ ][ ]
if self.Randomindex == 1:
    self.ChangeNumberImage(self.right_Number_LineEdit_3, 3, -1)
    self.ChangeNumberImage(self.right_Number_LineEdit_4, 4, -1)
# [ ] + [ ] = [1][2]
else:
    self.ChangeNumberImage(self.right_Number_LineEdit_1, 1, -1)
    self.ChangeNumberImage(self.right_Number_LineEdit_2, 2, -1)





class DialogDemo(QMainWindow):
    def __init__(self,parent=None):
        super(DialogDemo, self).__init__(parent)
        #设置主界面的标题及初始大小
        self.setWindowTitle('Dialog例子')
        self.resize(350,300)

        #创建按钮，注意()内的self必不可少，用于加载自身的一些属性设置
        self.btn=QPushButton(self)
        #设置按钮的属性：文本，移动位置，链接槽函数
        self.btn.setText('弹出对话框')
        self.btn.move(50,50)
        self.btn.clicked.connect(self.ShowDialog2)

        self.labelgif = QLabel(self)
        self.labelgif.setGeometry(QtCore.QRect(100,100,100,100))
        # self.labelgif.move(100,100)
        self.labelgif2 = QLabel(self)
        self.labelgif2.setGeometry(QtCore.QRect(200,200,200,200))
        self.gif = QMovie('../images/箭头动态.gif')
        self.gif.setScaledSize(QSize(100, 100))
        self.gif.setCacheMode(QMovie.CacheNone)
        self.labelgif.setMovie(self.gif)
        self.gif.start()
        self.gif.stateChanged.connect(lambda :self.gifshow(self.gif))


        # self.gif.stop()
        self.labelgif2.setMovie(self.gif)
        self.gif.start()


    def gifshow(self,gif):
        state = gif.state()
        print("state:",state)
        if state == gif.Running:
            print("Runing")
            return
        else:
            print("NoRuing")
            gif.start()


    def ShowDialog3(self):
        print("ShowDialog3")
        self.gif = QMovie('../images/箭头动态.gif')
        self.gif.setScaledSize(QSize(100, 100))
        self.labelgif.setMovie(self.gif)
        self.gif.stateChanged.connect(lambda: self.gifshow(self.gif))
        self.gif.start()
        self.btn.clicked.disconnect(self.ShowDialog3)
        self.btn.clicked.connect(self.ShowDialog2)

    def ShowDialog2(self):
        print("ShowDialog2")
        self.gif = QMovie('')
        self.labelgif.setMovie(self.gif)
        self.btn.clicked.disconnect(self.ShowDialog2)
        self.btn.clicked.connect(self.ShowDialog3)

    def SetDifficulty(self,s):
        print(s)

    def ShowDialog(self):
        self.Exdialog = QDialog()

        self.Exdialog.resize(420,250)
        self.Exdialog.setFixedSize(420,300)

        self.ExdialogWidget = QWidget(self.Exdialog)
        self.ExdialogWidget.resize(420,300)
        self.ExdialogWidget.setFixedSize(420,300)
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
        self.label1_LineEdit.setText("60")
        self.label1_LineEdit.setAlignment(Qt.AlignCenter)
        self.label1_LineEdit.setReadOnly(True)

        self.label2_LineEdit = QLineEdit(self.ExdialogWidget)
        self.label2_LineEdit.setGeometry(QtCore.QRect(190, 130, 100, 40))
        self.label2_LineEdit.setText("10")
        self.label2_LineEdit.setAlignment(Qt.AlignCenter)
        self.label2_LineEdit.setReadOnly(True)

        self.sbutton = QPushButton(self.ExdialogWidget)
        self.sbutton.setText("确定")
        self.sbutton.clicked.connect(self.Exdialog.close)
        self.sbutton.setGeometry(QtCore.QRect(280,230,100,40))
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

        self.Exdialog.exec()

    def time_reduce(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 30:
            return
        else:
            self.Timing -= 10
            self.label1_LineEdit.setText(str(self.Timing))

    def time_add(self):
        self.Timing = int(self.label1_LineEdit.text())
        if self.Timing == 300:
            return
        else:
            self.Timing += 10
            self.label1_LineEdit.setText(str(self.Timing))
        return

    def Number_reduce(self):
        self.NumberQuestions = int(self.label2_LineEdit.text())
        if self.NumberQuestions == 10:
            return
        else:
            self.NumberQuestions -= 10
            self.label2_LineEdit.setText(str(self.NumberQuestions))

    def Number_add(self):
        self.NumberQuestions = int(self.label2_LineEdit.text())
        if self.NumberQuestions == 30:
            return
        else:
            self.NumberQuestions += 10
            self.label2_LineEdit.setText(str(self.NumberQuestions))

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=DialogDemo()
    demo.show()
    sys.exit(app.exec_())