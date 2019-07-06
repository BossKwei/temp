import numpy as np
import tensorflow as tf
import gym
import random
import time


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def fc_layer(x, input_size, output_size, activation):
    W = weight_variable([input_size, output_size])
    b = bias_variable([output_size])
    y = tf.matmul(x, W) + b
    y = activation(y)
    return y


class DQN:
    NUM_EPISODES = 5000
    MAX_STEPS = 200
    LR = 0.1  # learning rate
    DF = 0.9  # discount factor

    def __init__(self):
        # model
        self.state = tf.placeholder(tf.float32, [None, 4])
        y1 = fc_layer(self.state, 4, 20, tf.nn.relu)
        self.q_predict = fc_layer(y1, 20, 2, tf.nn.relu)
        # loss
        self.action_mask = tf.placeholder(tf.float32, [None, 2])
        q_current = tf.reduce_sum(tf.multiply(self.q_predict, self.action_mask), axis=1)
        self.q_target = tf.placeholder(tf.float32, [None])
        loss = tf.reduce_mean(tf.squared_difference(q_current, self.q_target))
        # optimize
        self.train_step = tf.train.AdamOptimizer(1e-3).minimize(loss)
        #
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def train(self):
        env = gym.make('CartPole-v0')

        def random_action():
            return env.action_space.sample()

        #
        replay_list = []
        for episode in range(self.NUM_EPISODES):
            print("episode: ", episode)
            state = env.reset()
            for step in range(self.MAX_STEPS):
                action = self.choose_action(state) if random.random() > 0.8 else random_action()
                state_, reward, done, info = env.step(action)
                reward = -100.0 if done else reward
                replay_list.append([state, state_, action, reward, done])
                #
                if len(replay_list) >= 64:
                    replay_list.pop(0)
                    self.apply_training(replay_list)
                    # replay_list.clear()
                #
                state = state_
                if done:
                    break
        #
        for episode in range(1000):
            state = env.reset()
            for step in range(20000):
                print(step)
                action = self.choose_action(state)
                state_, reward, done, info = env.step(action)
                env.render()
                time.sleep(0.2)
                state = state_
                if done:
                    print('done')
                    break

    def apply_training(self, replay_list):
        state_batch = []
        state_next_batch = []
        action_batch = []
        reward_batch = []
        done_batch = []
        for row in replay_list:
            state, state_next, action, reward, done = row
            state_batch.append(state)
            state_next_batch.append(state_next)
            action_batch.append(action)
            reward_batch.append(reward)
            done_batch.append(done)
        # 1. q_values
        q_values_batch = self.sess.run(self.q_predict, feed_dict={self.state: state_next_batch})
        # 2. q_target
        q_target_batch = []
        for i in range(len(replay_list)):
            q_target_batch.append(reward_batch[i] if done_batch[i] else reward_batch[i] + self.DF * np.max(q_values_batch[i]))
        # 3. action mask
        action_mask_batch = []
        for action in action_batch:
            action_mask_batch.append([np.equal(action, i) for i in range(2)])
        # 4. train
        self.sess.run(self.train_step, feed_dict={self.state: state_batch,
                                                  self.action_mask: action_mask_batch,
                                                  self.q_target: q_target_batch})

    def choose_action(self, state):
        q_values = self.sess.run(self.q_predict, feed_dict={self.state: [state]})
        return np.argmax(q_values)


if __name__ == '__main__':
    # env = gym.make('CartPole-v0')
    # state = env.reset()
    # print(state)
    dqn = DQN()
    dqn.train()
