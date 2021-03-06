#coding=utf-8
#Version:python3.6.0
#Tools:Pycharm 2017.3.2
__date__ = ' 20:42'
__author__ = 'Colby'

####################
import cv2
import numpy as np
import fourierDescriptor as fd


def new_binaryMask(frame, x0, y0, width, height):
    cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0))  # 画出截取的手势框图
    roi = frame[y0:y0 + height, x0:x0 + width]  # 获取手势框图
    #cv2.imshow("roi", roi)  # 显示手势框图
    res = skinMask2(roi)  # 进行肤色检测
    cv2.imshow("res", res)  # 显示肤色检测后的图像

    ###############服饰膨胀##############################
    kernel = np.ones((3, 3), np.uint8)  # 设置卷积核
    erosion = cv2.erode(res, kernel)  # 腐蚀操作
    # cv2.imshow("erosion", erosion)
    dilation = cv2.dilate(erosion, kernel)  # 膨胀操作
    # cv2.imshow("dilation", dilation)

    ##############轮廓提取#######################################
    # binaryimg = cv2.Canny(res, 50, 200)  # 二值化，canny检测
    # h = cv2.findContours(binaryimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 寻找轮廓
    # contours = h[1]  # 提取轮廓
    # ret = np.ones(res.shape, np.uint8)  # 创建黑色幕布
    # cv2.drawContours(ret, contours, -1, (255, 255, 255), 1)  # 绘制白色轮廓
    # cv2.imshow("ret", ret)

    ret, fourier_result = fd.fourierDesciptor(dilation)
    #cv2.imshow("ret", ret)
    return ret

################方法一####################
####YCrCb颜色空间的Cr分量+Otsu法阈值分割算法
def skinMask1(roi):
    YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
    (y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
    cr1 = cv2.GaussianBlur(cr, (5,5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
    res = cv2.bitwise_and(roi,roi, mask = skin)
    return res

################方法二####################
####YCrCb颜色空间的Cr分量+Otsu法阈值分割算法
def skinMask2(roi):
	YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
	(y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
	cr1 = cv2.GaussianBlur(cr, (5,5), 0)
	_, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
	res = cv2.bitwise_and(roi,roi, mask = skin)
	return res
