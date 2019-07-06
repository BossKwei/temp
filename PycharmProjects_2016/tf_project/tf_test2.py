import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([3.0, 2.0])
y = tf.equal(a, b)


init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print(sess.run(y))
