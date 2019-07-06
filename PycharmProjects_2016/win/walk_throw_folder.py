import os
import numpy as np
import skimage.io, skimage.morphology, skimage.util
import sklearn.preprocessing


if __name__ == '__main__':
    x_data = []
    y_label = []
    #
    for root, dirs, files in os.walk('C:\\Users\\Mr.Trojan\\Desktop\\data_set', topdown=False):
        for file in files:
            print('.', end='')
            img_raw = skimage.io.imread(root + '\\' + file)
            img_dilated = skimage.morphology.dilation(img_raw)
            img_eroded = skimage.morphology.erosion(img_raw)
            img_raw_noised = skimage.util.random_noise(img_raw)
            img_dilated_noised = skimage.util.random_noise(img_dilated)
            img_eroded_noised = skimage.util.random_noise(img_eroded)
            y = int(root[-1])
            #
            x_data.append(img_raw)
            y_label.append(y)
            x_data.append(img_dilated)
            y_label.append(y)
            x_data.append(img_eroded)
            y_label.append(y)
            x_data.append(img_raw_noised)
            y_label.append(y)
            x_data.append(img_dilated_noised)
            y_label.append(y)
            x_data.append(img_eroded_noised)
            y_label.append(y)
        print('')
    #
    print(len(x_data))
    print(len(y_label))
    #
    x_data = np.array(x_data)
    print(x_data.shape)
    # print(x_data[0])
    x_data = np.reshape(x_data, [-1, 28*28])
    # print(x_data[0])
    #
    print(x_data.shape)
    #
    x_data = sklearn.preprocessing.MinMaxScaler().fit_transform(x_data)
    print(type(x_data))
    print(x_data.shape)
    #
    np.savetxt('C:\\Users\\Mr.Trojan\\Desktop\\data_set\\x_data.csv', x_data, delimiter=',')
    np.savetxt('C:\\Users\\Mr.Trojan\\Desktop\\data_set\\y_label.csv', y_label, delimiter=',')
    #
    print(np.min(x_data))

    dd = np.loadtxt('C:\\Users\\Mr.Trojan\\Desktop\\data_set\\y_label.csv', delimiter=',')
    pass