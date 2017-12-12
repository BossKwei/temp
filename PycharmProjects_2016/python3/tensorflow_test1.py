import numpy as np
import tensorflow as tf


v1 = tf.Variable(0, dtype=tf.float32)
step = tf.Variable(0, trainable=False)
ema = tf.train.ExponentialMovingAverage(0.99, step)
maintain_averages_op = ema.apply([v1])



sess = tf.Session()
sess.run(tf.global_variables_initializer())

sess.run(tf.assign(v1, 0.5))
sess.run(maintain_averages_op)
print(sess.run([v1, ema.average(v1)]))

sess.run(tf.assign(v1, -0.5))
sess.run(maintain_averages_op)
print(sess.run([v1, ema.average(v1)]))

sess.run(tf.assign(v1, -0.1))
sess.run(maintain_averages_op)
print(sess.run([v1, ema.average(v1)]))
