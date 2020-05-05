import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

class SwitchButton(QWidget):
    """自定义Switch按钮"""
    checkedChanged = pyqtSignal(bool)
    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)

        # 设置无边框和背景透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(80, 35)
        self.state = True  # 按钮状态：True表示开，False表示关

    def mousePressEvent(self, event):
        """鼠标点击事件：用于切换按钮状态"""
        super(SwitchButton, self).mousePressEvent(event)

        self.state = False if self.state else True
        self.checkedChanged.emit(self.state)
        self.update()

    def paintEvent(self, event):
        """绘制按钮"""
        super(SwitchButton, self).paintEvent(event)

        # 创建绘制器并设置抗锯齿和图片流畅转换
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # 定义字体样式
        font = QFont('Microsoft YaHei')
        font.setPixelSize(16)
        painter.setFont(font)

        # 开关为开的状态
        if self.state:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#6CC6CB'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)

            # 绘制圆圈
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.drawRoundedRect(45, 3, 30, 30, 16, 16)

            # 绘制文本
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(18, 6, 50, 20), Qt.AlignLeft, '开')
        # 开关为关的状态
        else:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#C3C3C3'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height()//2, self.height()//2)

            # 绘制圆圈
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.drawRoundedRect(3, 3, 30, 30, 16, 16)

            # 绘制文本
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(45, 6, 50, 20), Qt.AlignLeft, '关')


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(400,200)
        self.switchBtn = SwitchButton(self)
        self.switchBtn.setGeometry(10,10,80,35)
        self.switchBtn.checkedChanged.connect(self.getState)
        # self.status = self.statusBar()
        # self.status.showMessage("this is a example", 5000)
        # self.setWindowTitle("PyQt")

    def getState(self,checked):
        print("checked=", checked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    #form = SwitchBtn()
    form.show()
    sys.exit(app.exec_())
