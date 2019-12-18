#coding=utf-8
#Version:python3.6.0
#Tools:Pycharm 2017.3.2
__date__ = ' 20:27'
__author__ = 'Colby'

from finger_train import *

path = "fingertest"
#################模型测试######################
def finger_init():
    image_width = 100
    image_height = 100
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

finger_model = loadCNN_second()
finger_model.load_weights("model/model_2019_11_20_test.hdf5")
x_test,y_test = finger_init()
preds = finger_model.evaluate(x = x_test, y = y_test)
print("Loss = " + str(preds[0]))
print("Test Accuracy = " + str(preds[1]))