

###############模型训练##################################

import os
import cv2 as cv
import numpy as np
import pandas as pd
import random

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.utils import np_utils

from keras.utils.np_utils import *
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten
from keras.layers import Conv2D,MaxPool2D,ZeroPadding2D
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import load_model
from keras import backend as K
import matplotlib.pyplot as plt
K.backend()
import tensorflow as tf


class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('accuracy'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_accuracy'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('accuracy'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_accuracy'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        # if loss_type == 'epoch':
            # val_acc
        plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
        plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()




data_path = "fingertrain"
path = "fingertest"
image_width = 0
image_height = 0
# def initializers():
#     i = 0
#     x_data = []
#     y_data = []
#     for i in range(9):
#         dir = data_path+"/"+"roiimage_finger" + str(i)
#         walk = list(os.walk(dir))[0][2]
#         for name in walk:
#             png_name = dir+"/"+name
#             one_image = cv.imread(png_name)
#             cv.imshow("test",one_image)
def finger_init():
    print("image_width,image_height",image_width,image_height)
    x_data = []
    y_data = []
    i = 1
    dir_list = list(os.walk(path))[0][1]
    for dir in dir_list:
        one_dir = os.path.join(path, dir)
        dir_name = list(os.walk(one_dir))[0][2]
        print("dir_name:",one_dir)
        for png_name in dir_name:
            name = os.path.join(one_dir, png_name)
            one_image = cv.imread(name,0)
            one_image = cv.resize(one_image, (image_width, image_height))

            one_image = np.array(one_image)
            x_data.append(one_image)
            y_data.append(i)
            # cv.imshow("one_image",one_image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
        i = i + 1

    randnum = random.randint(0, 1000)
    random.seed(randnum)
    random.shuffle(x_data)
    random.seed(randnum)
    random.shuffle(y_data)

    x_data = np.array(x_data,dtype='f')
    x_data = x_data/255.0
    y_data = np.array(y_data)

    y_data = to_categorical(y_data,num_classes=10)
    print(x_data.shape)
    # for i in range(2700):
    #     print("y_data:",i,y_data[i])
    # print("y_data.shape:",y_data.shape)
    print(image_width,image_height)
    x_data = x_data.reshape([-1,image_width,image_height,1])
    print(x_data.shape)

    return x_data,y_data


def initializers():
    x_data = []
    y_data = []
    i = 0
    dir_list = list(os.walk(data_path))[0][1]
    for dir in dir_list:
        one_dir = os.path.join(data_path, dir)
        dir_name = list(os.walk(one_dir))[0][2]
        print("dir_name:",one_dir)
        for png_name in dir_name:
            name = os.path.join(one_dir, png_name)
            one_image = cv.imread(name,0)
            one_image = cv.resize(one_image, (image_width, image_height))

            one_image = np.array(one_image)
            x_data.append(one_image)
            y_data.append(i)
            # cv.imshow("one_image",one_image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
        i = i + 1

    randnum = random.randint(0, 1000)
    random.seed(randnum)
    random.shuffle(x_data)
    random.seed(randnum)
    random.shuffle(y_data)

    x_data = np.array(x_data,dtype='f')
    x_data = x_data/255.0
    y_data = np.array(y_data)

    y_data = to_categorical(y_data,num_classes=10)
    # for i in range(2700):
    #     print("y_data:",i,y_data[i])
    # print("y_data.shape:",y_data.shape)
    for i in range(2700):
        print("y_data:",i,y_data[i])
    print("***************************",image_width,image_height)
    x_data = x_data.reshape([-1,image_width,image_height,1])
    print(x_data.shape)

    return x_data,y_data

def loadCNN_second():
    global image_width
    global image_height
    global get_output
    image_width = 100
    image_height = 100
    model = Sequential()
    model.add(Conv2D(8,(4,4),padding="same",input_shape=(image_width,image_height,1)))
    convout1 = Activation("relu")
    model.add(convout1)
    model.add(MaxPool2D(pool_size=(4, 4)))
    model.add(Conv2D(16, (2, 2),padding="same"))
    convout2 = Activation("relu")
    model.add(convout2)
    model.add(MaxPool2D(pool_size=(2, 2),padding="same"))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(512))
    # model.add(Activation("relu"))
    # model.add(Dropout(0.5))
    # model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy",optimizer="adadelta",metrics=['accuracy'])
    model.summary()
    model.get_config()
    layer = model.layers[11]
    get_output = K.function([model.layers[0],input,K.learning_phase()],[layer.output,])
    return model


def loadCNN():
    global image_width
    global image_height
    image_width = 300
    image_height = 300
    global get_output
    model = Sequential()
    model.add(Conv2D(32,(5,5),padding="valid",input_shape=(image_width,image_height,1)))
    convout1 = Activation("relu")
    model.add(convout1)
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Conv2D(64,(3,3)))
    convout2 = Activation("relu")
    model.add(convout2)
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Conv2D(64,(5,5)))
    convout3 = Activation("relu")
    model.add(convout3)
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Conv2D(64,(5,5)))
    convout4 = Activation("relu")
    model.add(convout4)
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy",optimizer="adadelta",metrics=['accuracy'])
    model.summary()
    model.get_config()
    layer = model.layers[11]
    get_output = K.function([model.layers[0],input,K.learning_phase()],[layer.output,])
    return model

history = LossHistory()
def trainModel(model):
    x_data,y_data = initializers()
    x_test,y_test = finger_init()
    x_train = x_data[:x_data.shape[0]]
    y_train = y_data[:y_data.shape[0]]
    print("shape[0]:%d,%d",x_data.shape[0],y_data.shape[0])
    print("x_train.shape,y_train.shape",x_train.shape,y_train.shape)
    # hist = model.fit(x_train,y_train,batch_size = 100, epochs=100,verbose=1,validation_split=0.2,alidation_data=(x_test, y_test),callbacks=[history])
    hist = model.fit(x_train, y_train, batch_size=10, epochs=50, verbose=1,validation_split=0.2, callbacks=[history],shuffle=True)
    model.save_weights("model/model_2019_11_20_test.hdf5",overwrite=True)
    # 模型评估
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    # 绘制acc-loss曲线
    history.loss_plot('epoch')
    # history.loss_plot('batch')


# def new_test():
#     test_list = []
#     model = loadCNN()
#     model.load_weights("model/model.hdf5")
#     test_img = cv.imread("n7.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n40.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n67.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n107.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n126.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n168.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n193.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n237.png",0)
#     test_list.append(test_img)
#     test_img = cv.imread("n303.png",0)
#     test_list.append(test_img)
#
#     #h,w = test_img.shape
#     test_list = np.array(test_list,dtype='f')
#     test_list = test_list / 255.0
#     print(test_list.shape)
#     test_list = test_list.reshape([-1,300,300,1])
#     print(test_list.shape)
#     pdt = model.predict(test_list)
#     print(pdt.shape)
#     print(np.argmax(pdt,axis=1)+1)

if __name__ == "__main__":
    # 测试模型
    # new_test()

    # 训练模型
    # #
    mymodel = loadCNN_second()
    mymodel.load_weights("model/model_2019_11_20_test.hdf5")
    trainModel(mymodel)
