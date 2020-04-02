import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import random
from finger_train import *
import picture as pic
import cv2

# 手势识别的模块的文件地址
Model_Path = "../model/model_2020_02_22_test.hdf5"
# 正常大小无衬线字体
font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1
# ROI框的显示位置
x0 = 350
y0 = 40
# 录制的手势图片大小
width = 280
height = 280


class VideoThread(QThread):
    timer = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.result = 0

    ShowFlag = False
    def SetShowFlag(self,flag):
        self.ShowFlag = flag

    def work(self):
        self.timer.emit(int(self.result))

    def Getvalue(self,frame,res,finger_model):
        out = 0
        """这里可以插入代码调用网络"""
        test_image = res
        test_image = cv.resize(test_image, (300, 300))
        test_image = np.array(test_image, dtype='f')
        test_image = test_image / 255.0
        test_image = test_image.reshape([-1, 300, 300, 1])
        pdt = finger_model.predict(test_image)
        out = np.argmax(pdt, axis=1)
        cv2.putText(frame, "the finger is: %d" % out, (x0, y0), font, fontsize, (0, 0, 255))  # 标注字体
        return out,res


    def Getresult(self,frame, x0, y0, width, height, finger_model):
        # 得到处理后的照片
        res = pic.new_binaryMask(frame, x0, y0, width, height)

        return self.Getvalue(frame, res, finger_model)
        # out = 0
        # """这里可以插入代码调用网络"""
        # test_image = res
        # test_image = cv.resize(test_image, (300, 300))
        # test_image = np.array(test_image, dtype='f')
        # test_image = test_image / 255.0
        # test_image = test_image.reshape([-1, 300, 300, 1])
        # pdt = finger_model.predict(test_image)
        # out = np.argmax(pdt, axis=1)
        # cv2.putText(frame, "the finger is: %d" % out, (x0, y0), font, fontsize, (0, 0, 255))  # 标注字体

    def startvideo(self,finger_model):
        # 开启摄像头
        cap = cv2.VideoCapture(0)

        self.lst = [0] * 20
        self.index = 0

        while (True):
            # 读帧
            ret, frame = cap.read()
            # 图像翻转
            frame = cv2.flip(frame, 2)
            # 显示ROI区域  #调用函数

            # 获得图像预测的数值
            VideoNumber,res= self.Getresult(frame, x0, y0, width, height, finger_model)


            if self.index != 20:
                self.lst[self.index] = int(VideoNumber)
            else:
                self.index = 0
                self.lst[self.index] = int(VideoNumber)

            self.index += 1
            self.result = np.argmax(np.bincount(self.lst))
            # print("lst",self.lst," maxnumber:",self.result)

            # 等待键盘输入
            key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
            #     break

            if self.ShowFlag == True:
                frame = frame[y0 - 30:y0 + height + 100, x0 - 100:x0 + width]
                cv2.imshow("maomilaoshi", frame)
                cv2.imshow("res",res)
            else:
                cv2.destroyWindow("maomilaoshi")
                cv2.destroyWindow("res")


        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        global Model_Path
        finger_model = loadCNN()
        finger_model.load_weights(Model_Path)
        self.startvideo(finger_model)


VideoSingleton = VideoThread()