import os
import numpy as np
import scipy.stats
import skimage.io, skimage.color, skimage.morphology, skimage.util
import matplotlib.pyplot as plt


def fuck_white_edge(img):
    rows, cols = img.shape
    for row in range(rows):
        entropy = scipy.stats.entropy(img[row, :])
        if entropy > 3.0 and (row < 3 or row > 24):
            img[row, :] = 0
    for col in range(cols):
        entropy = scipy.stats.entropy(img[:, col])
        if entropy > 3.0 and (col < 3 or col > 24):
            img[:, col] = 0
    return img


def edge_and_hist(img):
    rows, cols = img.shape
    entropy = []
    for row in range(rows):
        entropy.append(scipy.stats.entropy(img[row, :]))
    print(entropy)
    entropy = []
    for col in range(cols):
        entropy.append(scipy.stats.entropy(img[:, col]))
    print(entropy)
    return img


# img = skimage.io.imread('/home/bosskwei/Desktop/22.bmp')
# img = edge_and_hist(img)

#skimage.io.imshow(img)
#skimage.io.show()

x_data = []
y_label = []

for root, dirs, files in os.walk('/home/bosskwei/Desktop/data_set', topdown=False):
    for file in files:
        print('.', end='')
        img = skimage.io.imread(root + '/' + file)
        img_dilated = skimage.morphology.dilation(img, skimage.morphology.square(3))
        img_eroded = skimage.morphology.erosion(img, skimage.morphology.square(3))
        img_noised = skimage.util.random_noise(img)
        y = int(root[-1])
        #
        x_data.append(img)
        y_label.append(y)
        x_data.append(img_dilated)
        y_label.append(y)
        x_data.append(img_eroded)
        y_label.append(y)
        x_data.append(img_noised)
        y_label.append(y)
    print('')

print(len(x_data))
print(len(y_label))

x_data = np.array(x_data, dtype=np.float32)
x_data = x_data / 255.0
a_min = x_data.min()
a_max = x_data.max()
x_data = np.reshape(x_data, [-1, 28*28])
y_label = np.eye(10)[y_label]
y_label = np.array(y_label, dtype=np.float32)

print(x_data.shape)
print(y_label.shape)


from tensorflow.examples.tutorials.mnist import input_data


mnist = input_data.read_data_sets('/tmp', one_hot=True)
x_mnist, y_mnist = mnist.train.next_batch(50000)

x_mnist = np.array(x_mnist, dtype=np.float32)
y_mnist = np.array(y_mnist, dtype=np.float32)

x = np.concatenate([x_data, x_mnist])
y = np.concatenate([y_label, y_mnist])

print(x.shape)
print(y.shape)

np.savetxt('/home/bosskwei/Desktop/mnist_x.csv', x)
np.savetxt('/home/bosskwei/Desktop/mnist_y.csv', y)



'''
for root, dirs, files in os.walk('/home/bosskwei/Desktop/data_set', topdown=False):
    for file in files:
        img = skimage.io.imread(root + '/' + file)
        img = skimage.color.rgb2gray(img)
        img = fuck_white_edge(img)
        skimage.io.imsave(root + '/' + file, img)
        print('.')
'''
