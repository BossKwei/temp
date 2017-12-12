import tensorflow as tf
import numpy as np
from sklearn import preprocessing
import random

####################################
csv_raw_data = np.loadtxt(open('list_of_us_states_data.csv', 'rb'), delimiter=',', skiprows=1,  usecols=[1,2,3,4,5,6,7,8,9,10,11,12]) # used col - flag
#print(csv_raw_data.shape)
filtered_data = preprocessing.StandardScaler().fit_transform(csv_raw_data)
####################################
y_label_2 = preprocessing.MinMaxScaler().fit_transform(csv_raw_data[:,0:2])
x_data = csv_raw_data[:,2:12]
#print(y_label_2.shape)
#print(x_data.shape)
y_label = y_label_2[:,0] + y_label_2[:,1]
y_label = preprocessing.MinMaxScaler().fit_transform(y_label)
####################################
np.savetxt('y_label.csv', y_label)
np.savetxt('y_label_2.csv', y_label_2)
np.savetxt('x_data.csv', x_data)
####################################
x_train = x_data[0:40]
x_test = x_data[40:50]
y_train = y_label[0:40]
y_test = y_label[40:50]
####################################


def get_batch_15():
    index = [i for i in range(40)]
    random.shuffle(index)
    x0 = []
    y0 = []
    for i in range(15):
        x0.append(x_train[index[i]])
        y0.append(y_train[index[i]])
    return np.array(x0), np.array(y0).reshape([15, 1])


def get_test_10():
    x0 = []
    y0 = []
    for i in range(10):
        x0.append(x_train[i])
        y0.append(y_train[i])
    return np.array(x0), np.array(y0).reshape([10, 1])


x = tf.placeholder(tf.float32, [None, 10])
W = tf.Variable(tf.zeros([10, 1]))
b = tf.Variable(tf.zeros([1]))
y = tf.sigmoid(tf.matmul(x, W) + b)

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 1])

# The raw formulation of cross-entropy,
#
#   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
#                                 reduction_indices=[1]))
#
# can be numerically unstable.
#
# So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
# outputs of 'y', and then average across the batch.
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
error_level = tf.reduce_mean(tf.abs(y - y_))

sess = tf.InteractiveSession()
# Train
tf.global_variables_initializer().run()
for _ in range(100):
    batch_xs, batch_ys = get_batch_15()
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    print(sess.run(error_level, feed_dict={x: batch_xs, y_: batch_ys}))


# Test trained model
batch_xs, batch_ys = get_test_10()
print(sess.run(error_level, feed_dict={x: batch_xs,
                                    y_: batch_ys}))