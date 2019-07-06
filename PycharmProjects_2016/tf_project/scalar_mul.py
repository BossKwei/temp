import argparse
import sys
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import time


a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0]])
# y = tf.multiply(a , b)
y = tf.matmul(a, b)


init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print(sess.run(y))