from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *



class ContactUs(object):
    def __init__(self,parents):
        super().__init__()
        self.frame = QWidget(parents)
        self.frame.setObjectName("Frame")
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(1200, 900)

        self.init_frame()

    def init_frame(self):
        self.pushButton_1 = QtWidgets.QPushButton("正常考试模式", self.frame)
        self.pushButton_1.setObjectName("HomeButton")
        # self.pushButton_1.setIcon(QIcon("../images/考试.png"))
        self.pushButton_1.setFixedSize(300, 50)
        self.pushButton_1.move(450,700)
        self.pushButton_1.setText("返回主菜单")

        self.LineEdit_1 = QLineEdit(self.frame)
        self.LineEdit_1.setFixedSize(800, 50)
        self.LineEdit_1.move(200,400)

        self.LineEdit_2 = QLineEdit(self.frame)
        self.LineEdit_2.setFixedSize(800, 50)
        self.LineEdit_2.move(200,500)

        self.LineEdit_1.setAlignment(Qt.AlignCenter)
        self.LineEdit_2.setAlignment(Qt.AlignCenter)
        self.LineEdit_1.setStyleSheet("color:black;font:25px;background:transparent;border-width:0;border-style:outset")
        self.LineEdit_2.setStyleSheet("color:black;font:25px;background:transparent;border-width:0;border-style:outset")
        self.LineEdit_1.setReadOnly(True)
        self.LineEdit_2.setReadOnly(True)
        self.LineEdit_1.setText("如果在使用过程中遇到问题或着有改进的建议，可通过以下方式联系我们")
        self.LineEdit_2.setText("425185455@qq.com")


        self.frame.setStyleSheet('''
            QPushButton{border:none;color:white;font-size:30px}
            QPushButton:hover{
                    border-left:4px solid white;
                    font-size:35px;
                    background:#4affa5;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
            
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