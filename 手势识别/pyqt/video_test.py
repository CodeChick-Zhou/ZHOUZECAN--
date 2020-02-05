
###################前置摄像头测试###########################
from finger_train import *
# from PyQt5 import QtCore,QtGui,QtWidgets
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from PyQt5.QtCore import *
import picture as pic
import cv2

# # 正常大小无衬线字体
# font = cv2.FONT_HERSHEY_SIMPLEX
# fontsize = 1
# # ROI框的显示位置
# x0 = 330
# y0 = 40
# # 录制的手势图片大小
# width = 300
# height = 300
#
#
#
#
#
# class VideoThread(QThread):
#     timer = pyqtSignal()
#
#     def Getbinary(self,frame, x0, y0, width, height, finger_model):
#         # 得到处理后的照片
#         res = pic.new_binaryMask(frame, x0, y0, width, height)
#
#         out = 0
#         """这里可以插入代码调用网络"""
#         test_image = res
#         test_image = cv.resize(test_image, (300, 300))
#         test_image = np.array(test_image, dtype='f')
#         test_image = test_image / 255.0
#         test_image = test_image.reshape([-1, 300, 300, 1])
#         pdt = finger_model.predict(test_image)
#         out = np.argmax(pdt, axis=1)
#         cv2.putText(frame, "the finger is: %d" % out, (x0, y0), font, fontsize, (0, 255, 0))  # 标注字体
#         return out
#
#     def startvideo(self,finger_model):
#         # 开启摄像头
#         cap = cv2.VideoCapture(0)
#         i = 0
#         while (True):
#             # 读帧
#             ret, frame = cap.read()
#             # 图像翻转
#             frame = cv2.flip(frame, 2)
#             # 显示ROI区域  #调       用函数
#             roi = self.Getbinary(frame, x0, y0, width, height, finger_model)
#
#             i += 1
#             if i == 50:
#                 self.timer.emit(5)
#             # 等待键盘输入
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 break
#             cv2.imshow("frame", frame)
#
#         cap.release()
#         cv2.destroyAllWindows()
#
#     def run(self):
#         finger_model = loadCNN()
#         finger_model.load_weights("model/model_2019_11_20_best.hdf5")
#         self.startvideo(finger_model)
