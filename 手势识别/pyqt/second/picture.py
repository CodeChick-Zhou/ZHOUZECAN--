
####################
import cv2
import numpy as np
import fourierDescriptor as fd


def new_Canny(dilation,res):
    gray = cv2.cvtColor(dilation, cv2.COLOR_RGB2GRAY)
    cv2.imshow("gray", gray)
    ret, s = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow("s", s)
    binaryimg = cv2.Canny(s, 50, 200)  # 二值化，canny检测
    cv2.imshow("binaryimg", binaryimg)
    h = cv2.findContours(binaryimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 寻找轮廓
    contour = h[1]
    contour = sorted(contour, key=cv2.contourArea, reverse=True)

    # area = []
    # # print(h[1])
    # for k in range(len(h[1])):
    #     print(k)
    #     area.append(cv2.contourArea(h[1][k]) )
    # max_idx = np.argmax(np.array(area))

    contours = contour[0]  # 提取轮廓
    # print(contours)
    ret = np.ones(res.shape, np.uint8)  # 创建黑色幕布
    cv2.drawContours(ret, contours, -1, (255, 255, 255), 1)  # 绘制白色轮廓
    cv2.imshow("ret", ret)
    ret = cv2.Canny(ret, 50, 200)  # 二值化，canny检测r
    print(ret.shape)
    cv2.imshow("ret1", ret)

    return ret


def new_binaryMask(frame, x0, y0, width, height):
    cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0))  # 画出截取的手势框图
    roi = frame[y0:y0 + height, x0:x0 + width]  # 获取手势框图

    #cv2.imshow("roi", roi)  # 显示手势框图
    res = skinMask2(roi)  # 进行肤色检测
    # cv2.imshow("肤色检测后的图像", res)  # 显示肤色检测后的图像

    ###############服饰膨胀##############################
    kernel = np.ones((3, 3), np.uint8)  # 设置卷积核
    erosion = cv2.erode(res, kernel)  # 腐蚀操作
    # cv2.imshow("erosion", erosion)
    dilation = cv2.dilate(erosion, kernel)  # 膨胀操作
    # cv2.imshow("dilation", dilation)
    #
    # ##############轮廓提取#######################################
    # ret = new_Ca nny(dilation,res)

    # print(dilation.shape)
    ret, descirptor_in_use = fd.fourierDesciptor(dilation)
    black = fd.reconstruct(dilation,descirptor_in_use)

    # print(ret.shape)
    # cv2.imshow("black", black)
    # cv2.imshow("ret", ret)
    # print("fourier_result",fourier_result)
    # cv2.imshow("fourier_result", fourier_result)
    # print(ret_image.shape)
    # cv2.imshow("ret_image", ret_image)
    # cv2.imshow("fourier_result", fourier_result)
    return ret

################方法一####################
#########椭圆肤色检测模型##########
def skinMask1(roi):
    skinCrCbHist = np.zeros((256,256), dtype= np.uint8)
    cv2.ellipse(skinCrCbHist, (113,155),(23,25), 43, 0, 360, (255,255,255), -1) #绘制椭圆弧线
    YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
    (y,Cr,Cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
    skin = np.zeros(Cr.shape, dtype = np.uint8) #掩膜
    (x,y) = Cr.shape
    for i in range(0, x):
        for j in range(0, y):
            if skinCrCbHist [Cr[i][j], Cb[i][j]] > 0: #若不在椭圆区间中
                skin[i][j] = 255
    res = cv2.bitwise_and(roi,roi, mask = skin)
    return res

################方法二####################
####YCrCb颜色空间的Cr分量+Otsu法阈值分割算法#
def skinMask2(roi):
    YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
    (y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
    cr1 = cv2.GaussianBlur(cr, (5,5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
    res = cv2.bitwise_and(roi,roi, mask = skin)
    return res

##########方法三###################
########HSV颜色空间H范围筛选法######
def skinMask3(roi):
	low = np.array([0, 48, 50]) #最低阈值
	high = np.array([20, 255, 255]) #最高阈值
	hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) #转换到HSV空间
	mask = cv2.inRange(hsv,low,high) #掩膜，不在范围内的设为255
	res = cv2.bitwise_and(roi,roi, mask = mask) #图像与运算
	return res