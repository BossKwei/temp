import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


mnist = input_data.read_data_sets('/tmp', one_hot=True)
x, y = mnist.train.next_batch(50000)

x = np.array(x, dtype=np.float32)
y = np.array(y, dtype=np.float32)

np.savetxt('/home/bosskwei/Desktop/mnist_x.csv', x)
np.savetxt('/home/bosskwei/Desktop/mnist_y.csv', y)