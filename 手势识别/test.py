#coding=utf-8
#Version:python3.6.0
#Tools:Pycharm 2017.3.2
__date__ = ' 17:11'
__author__ = 'Colby'



######################随意测试#############################
import random
import numpy as np
import cv2 as cv

a = cv.imread("finger1_train2.png")
print(a.shape)
cv.imshow("a1",a)
a = cv.resize(a,(100,100))
print(a.shape)
cv.imshow("a2",a)
cv.waitKey(0)
cv.destroyAllWindows()