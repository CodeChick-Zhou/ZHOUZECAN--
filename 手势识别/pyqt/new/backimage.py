from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from GetFileName import *
import sys



class backimage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('首页')
        self.resize(1200, 900)
        self.setFixedSize(self.width(), self.height())

        self.frame = QWidget(self)
        self.frame.resize(1200, 900)
        self.frame.setFixedSize(self.width(), self.height())
        self.frame.setObjectName("Frame")

        self.readfile()
        self.frame.setStyleSheet("QWidget#Frame{border-image:url("+self.path[self.curpathindex]+");}")

        self.label_star = QLabel(self.frame)
        self.label_star.setGeometry(QtCore.QRect(20, 20, 40, 40))
        self.label_star.setPixmap(QPixmap("../images/star.png"))
        self.label_star.setScaledContents(True)  # 让图片自适应label大小

        self.LineEdit_star = QLineEdit(self.frame)
        self.LineEdit_star.setGeometry(QtCore.QRect(70, 25, 80, 30))
        self.LineEdit_star.setReadOnly(True)
        self.LineEdit_star.setStyleSheet('''
                                        background: rgb(230,230,230);
                                        border-radius: 5px;
                                        border:1px solid rgb(180, 180, 180);
                                        font-size:25px
                                        ''')
        self.LineEdit_star.setText(self.curstars)
        self.LineEdit_star.setAlignment(Qt.AlignCenter)

        self.backbutton = QPushButton("退出",self.frame)
        self.backbutton.setGeometry(QtCore.QRect(1050, 20, 120, 50))
        self.backbutton.setStyleSheet('''
            QPushButton{
                    background:#ff3c3c;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
            }
            QPushButton:hover{font-size:18px;background:red}
            ''')


        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap("../images/screen7.jpg").scaled(self.frame.size())))
        # self.frame.setPalette(palette)


        self.W_ICONSIZE = 320
        self.H_ICONSIZE = 240
        self.H_ICONITEM = 210
        # 创建QListWidget部件
        self.m_pListWidget = QListWidget(self.frame)
        self.m_pListWidget.setStyleSheet("background-color:transparent")
        self.m_pListWidget.setFrameShape(QListWidget.NoFrame)

        self.m_pListWidget.setGeometry(QtCore.QRect(0, 50, 1200, 900))
        # 设置QListWidget中的单元项的图片大小
        self.m_pListWidget.setIconSize(QtCore.QSize(self.W_ICONSIZE,self.H_ICONSIZE))
        self.m_pListWidget.setResizeMode(QListView.Adjust)
        # 设置QListWidget的显示模式
        self.m_pListWidget.setViewMode(QListView.IconMode)
        # 设置QListWidget中的单元项不可被拖动
        self.m_pListWidget.setMovement(QListView.Static)
        # 设置QListWidget中的单元项的间距
        self.m_pListWidget.setSpacing(40)

        for i in range(0,len(self.stars)):
            # 获得图片路径
            # 生成图像objPixmap
            objPixmap = QPixmap(self.path[i])
            # 生成QListWidgetItem对象(注意：其Icon图像进行了伸缩[96 * 96])---scaled函数
            pItem = QListWidgetItem(QIcon(objPixmap.scaled(QSize(self.W_ICONSIZE, self.H_ICONITEM))), "⭐ : "+self.stars[i])

            # 设置单元项的宽度和高度
            pItem.setSizeHint(QtCore.QSize(self.W_ICONSIZE, self.H_ICONSIZE))
            self.m_pListWidget.insertItem(i, pItem)


        # self.setCentralWidget(self.m_pListWidget)
        self.m_pListWidget.clicked.connect(self.check)  # 单击选中某一个选项
        # self.m_pListWidget.connect(itemClicked(self.m_pListWidget), self, SLOT(Slot_ItemClicked(QListWidgetItem *)))
        m_strPath = ""

        self.setWindowTitle("zzc")


    def readfile(self):
        file_name = 'backimage.txt'

        Firstflag = True
        self.path = []
        self.stars = []

        self.curstars = 0
        with open(file_name) as file_obj:
            for content in file_obj:
                if Firstflag:
                    self.curstars = content[6:-1]
                    Firstflag = False
                elif "curpathindex" in content:
                    cur = content.find(':')
                    self.curpathindex = int(content[cur+1:-1])
                    print("content[cur+1:-1]",content[cur+1:-1])
                else:
                    index = content.find(' ')
                    self.path.append(content[6:index - 1])
                    self.stars.append(content[index + 6:-1])

        print("self.curstars",self.curstars)
        print("self.path",self.path)
        print("self.stars",self.stars)

        # file_data = ""
        # with open(file_name) as file_obj:
        #     for content in file_obj:
        #         if self.path[0] in content:
        #             content = "path:\"../images/screen4\" stat:1\n"
        #         file_data += content
        #
        # with open(file_name, "w", encoding="utf-8") as f:
        #     f.write(file_data)
        # print(file_data)

    def check(self,index):
        r = index.row()
        print(r)

        if int(self.curstars) > int(self.stars[r]):
            self.frame.setStyleSheet("QWidget#Frame{border-image:url("+self.path[r]+");}")
            # palette = QPalette()
            # palette.setBrush(QPalette.Background, QBrush(QPixmap(self.path[r]).scaled(self.size())))
            # self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    backimage = backimage()
    backimage.show()
    sys.exit(app.exec_())
