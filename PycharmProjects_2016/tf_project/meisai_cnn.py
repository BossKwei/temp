import argparse
import sys
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


FLAGS = None


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def max_pool_8x2(x):
    return tf.nn.max_pool(x, ksize=[1, 8, 2, 1], strides=[1, 8, 2, 1], padding='SAME')


def max_pool_8x1(x):
    return tf.nn.max_pool(x, ksize=[1, 8, 1, 1], strides=[1, 8, 1, 1], padding='SAME')

def train():
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
    sess = tf.InteractiveSession()

    with tf.name_scope('input'):
        x = tf.placeholder(tf.float32, [None, 784])
        y_ = tf.placeholder(tf.float32, [None, 10])
        x_image = tf.reshape(x, [-1, 3200, 10, 1])

    with tf.name_scope('conv_1'):
        W_conv1 = weight_variable([9, 3, 1, 16])
        b_conv1 = bias_variable([16])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    with tf.name_scope('max_pool_1'):
        h_pool1 = max_pool_8x2(h_conv1)

    with tf.name_scope('conv_2'):
        W_conv2 = weight_variable([9, 3, 16, 32])
        b_conv2 = bias_variable([32])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    with tf.name_scope('max_pool_2'):
        h_pool2 = max_pool_8x1(h_conv2)

    with tf.name_scope('hidden_1'):
        W_fc1 = weight_variable([50 * 5 * 32, 80])
        b_fc1 = bias_variable([80])
        h_pool2_flat = tf.reshape(h_pool2, [-1, 50 * 5 * 32])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    with tf.name_scope('keep_probability'):
        keep_prob = tf.placeholder(tf.float32)

    with tf.name_scope('dropout'):
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('result'):
        W_fc2 = weight_variable([80, 1])
        b_fc2 = bias_variable([1])
        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    with tf.name_scope('loss'):
        with tf.name_scope('softmax'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv)
        with tf.name_scope('cross_entropy'):
            cross_entropy = tf.reduce_mean(cross_entropy)
    #tf.summary.scalar('cross_entropy', cross_entropy)

    with tf.name_scope('train'):
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    with tf.name_scope('debug'):
        with tf.name_scope('SOI'):
            correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        with tf.name_scope('accuracy'):
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        #tf.summary.scalar('accuracy', accuracy)

    with tf.name_scope('output'):
        with tf.name_scope('SOI'):
            correct_prediction = tf.reduce_mean(y_conv)

    '''
    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )
    '''
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(FLAGS.log_dir + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(FLAGS.log_dir + '/test')
    tf.global_variables_initializer().run()
    sess.run(tf.global_variables_initializer())

    '''for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            #
            train_accuracy = accuracy.eval(feed_dict={
                x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
            #
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        #
    print("test accuracy %g" % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))'''


def main(_):
    if tf.gfile.Exists(FLAGS.log_dir):
        tf.gfile.DeleteRecursively(FLAGS.log_dir)
    tf.gfile.MakeDirs(FLAGS.log_dir)
    train()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fake_data', nargs='?', const=True, type=bool,
                        default=False,
                        help='If true, uses fake data for unit testing.')
    parser.add_argument('--max_steps', type=int, default=1000,
                        help='Number of steps to run trainer.')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Initial learning rate')
    parser.add_argument('--dropout', type=float, default=0.9,
                        help='Keep probability for training dropout.')
    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                        help='Directory for storing input data')
    parser.add_argument('--log_dir', type=str, default='/tmp/tensorflow/mnist/logs/mnist_with_summaries',
                        help='Summaries log directory')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
