import numpy as np
import tensorflow as tf


# sgd batch
def get_batch(batch_size):
    x_batch = np.array([[1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1], ], dtype=np.float32)
    y_batch = np.array([[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]], dtype=np.float32)
    return x_batch, y_batch


def main():
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    # build network
    with tf.name_scope('input'):
        x = tf.placeholder(dtype=tf.float32, shape=[None, 7])

    with tf.name_scope('hidden'):
        W1 = weight_variable(shape=[7, 20])
        b1 = bias_variable(shape=[20])
        y1 = tf.nn.tanh(tf.matmul(x, W1) + b1)

    with tf.name_scope('output'):
        W2 = weight_variable(shape=[20, 1])
        b2 = bias_variable(shape=[1])
        y = tf.nn.tanh(tf.matmul(y1, W2) + b2)

    with tf.name_scope('loss'):
        y_ = tf.placeholder(dtype=tf.float32, shape=[None, 1])
        loss_func = tf.reduce_mean(
            tf.squared_difference(y, y_)
        )
        train_step = tf.train.AdamOptimizer().minimize(loss_func)

    # init tensorflow session
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    # save checkpoint
    saver = tf.train.Saver()

    # train network
    for step in range(100):
        x_batch, y_batch = get_batch(5)
        _, loss = sess.run([train_step, loss_func], feed_dict={x: x_batch, y_: y_batch})
        print('step: {step}, loss:{loss}'.format(step=step, loss=loss))

    # save network
    print('Model saved in file: {path}'.format(path=saver.save(sess=sess, save_path='./')))


if __name__ == '__main__':
    main()
