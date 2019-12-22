#coding=utf-8
#Version:python3.6.0
#Tools:Pycharm 2017.3.2
__date__ = ' 12:56'
__author__ = 'Colby'



###################前置摄像头测试###########################
from finger_train import *
import picture as pic
import cv2

# 正常大小无衬线字体
font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1
# ROI框的显示位置
x0 = 330
y0 = 40
# 录制的手势图片大小
width = 300
height = 300

def Getbinary(frame, x0, y0, width, height, finger_model):
    # 显示方框
    # cv2.rectangle(frame, (x0, y0), (x0+width, y0+height), (0, 255, 0))
    res = pic.new_binaryMask(frame, x0, y0, width, height)
    #提取ROI像素
    # roi = frame[y0:y0+height, x0:x0+width] #
    # gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # 高斯模糊 斯模糊本质上是低通滤波器，输出图像的每个像素点是原图像上对应像素点与周围像素点的加权和
    # 高斯矩阵的尺寸越大，标准差越大，处理过的图像模糊程度越大
    # blur = cv2.GaussianBlur(gray, (5, 5), 2) # 高斯模糊，给出高斯模糊矩阵和标准差

    # 当同一幅图像上的不同部分的具有不同亮度时。这种情况下我们需要采用自适应阈值
    # 参数： src 指原图像，原图像应该是灰度图。 x ：指当像素值高于（有时是小于）阈值时应该被赋予的新的像素值
    #  adaptive_method  指： CV_ADAPTIVE_THRESH_MEAN_C 或 CV_ADAPTIVE_THRESH_GAUSSIAN_C
    # block_size           指用来计算阈值的象素邻域大小: 3, 5, 7, ..
    #   param1           指与方法有关的参数    #
    # th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) # ret还是bool类型

    out = 0
    """这里可以插入代码调用网络"""
    test_image = res
    test_image = cv.resize(test_image,(100,100))
    test_image = np.array(test_image, dtype='f')
    test_image = test_image / 255.0
    test_image = test_image.reshape([-1, 100, 100, 1])
    pdt = finger_model.predict(test_image)
    out = np.argmax(pdt, axis=1)
    cv2.putText(frame, "the finger is: %d" % out, (x0, y0), font, fontsize, (0, 255, 0))  # 标注字体
    return res




def start_video(finger_model):
    cap = cv2.VideoCapture(0)

    while (True):
        # 读帧
        ret, frame = cap.read()
        # 图像翻转
        frame = cv2.flip(frame, 2)
        # 显示ROI区域  #调       用函数
        roi = Getbinary(frame, x0, y0, width, height,finger_model)

        # 等待键盘输入
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        cv2.imshow('frame', frame)
        cv2.imshow('ROI', roi)

    cap.release()
    cv2.destroyAllWindows()


finger_model = loadCNN_second()
finger_model.load_weights("model/model_2019_11_20_second.hdf5")
start_video(finger_model)

# 测试模型
# new_test()

# 训练模型
# mymodel = loadCNN()
# mymodel.load_weights("model/model.hdf5")
# trainModel(mymodel)