import time
import random
import numpy as np
import tensorflow as tf
import gym


class DQN:
    # Modeling
    STATE_SPACE = 4
    ACTION_SPACE = 2
    # Training
    LR = 1e-3  # learning rate

    def __init__(self):
        self.sess = tf.Session()
        # model
        with tf.name_scope('input'):
            self.state = tf.placeholder(tf.float32, [None, self.STATE_SPACE])
        with tf.name_scope('hidden1'):
            y1 = tf.layers.dense(self.state, units=20, activation=tf.nn.tanh)
        with tf.name_scope('hidden2'):
            y2 = tf.layers.dense(y1, units=10, activation=tf.nn.tanh)
        with tf.name_scope('output'):
            self.q_predict = tf.layers.dense(y2, units=self.ACTION_SPACE)
        # processing
        with tf.name_scope('processing'):
            self.action_mask = tf.placeholder(tf.float32, [None, self.ACTION_SPACE])
            q_current = tf.reduce_sum(tf.multiply(self.q_predict, self.action_mask), axis=1)
            self.q_target = tf.placeholder(tf.float32, [None])
        # loss
        with tf.name_scope('loss'):
            loss = tf.reduce_mean(tf.squared_difference(q_current, self.q_target))
            tf.summary.scalar('loss', loss)
        # optimize
        with tf.name_scope('train'):
            self.train_step = tf.train.AdamOptimizer(self.LR).minimize(loss)
        # tensor board
        self.merged = tf.summary.merge_all()
        self.train_writer = tf.summary.FileWriter('/tmp/qlearning_3/train', self.sess.graph)
        self.test_writer = tf.summary.FileWriter('/tmp/qlearning_3/test')
        # init
        self.sess.run(tf.global_variables_initializer())


class Agent:
    DF = 0.5

    def __init__(self):
        self.dqn = DQN()
        self.env = gym.make('CartPole-v0')
        #
        global_step = 0
        #
        self._state_batch = []
        self._q_target_batch = []
        self._action_mask_batch = []

    def observe(self, state, action, reward, done, state_):
        q_target = reward if done else reward + self.DF * np.max(self._get_q_values(state_))
        action_mask = [np.equal(action, i) for i in range(self.dqn.ACTION_SPACE)]

    def fit_network(self):
        summary, _ = self.dqn.sess.run([self.dqn.merged, self.dqn.train_step],
                                       feed_dict={self.dqn.state: self.state_batch,
                                                  self.dqn.action_mask: self.action_mask_batch,
                                                  self.dqn.q_target: self.q_target_batch})
        self.dqn.train_writer.add_summary(summary, self.global_step)

    def train(self, episodes=50, max_step=200):
        for episode in range(episodes):
            print("episode: ", episode)
            state = self.env.reset()
            #
            for step in range(max_step):
                # 1. predict
                action = self._choose_action_with_exploration(state)
                # 2. action
                state_, reward, done, info = self.env.step(action)
                reward = -100.0 if done else reward
                # 3. observe
                self.observe(state, action, reward, done, state_)
                # 4. update
                state = state_
                if done:
                    break
            #
            self.fit_network()

    def test(self, delay=0.2, episodes=1, max_step=100):
        for episode in range(episodes):
            state = self.env.reset()
            for step in range(max_step):
                print(step)
                action = self._choose_action(state)
                state_, reward, done, info = self.env.step(action)
                self.env.render()
                time.sleep(delay)
                state = state_
                if done:
                    print('done')
                    break

    def _get_q_values(self, state):
        q_values = self.dqn.sess.run(self.dqn.q_predict, feed_dict={self.dqn.state: [state]})
        return q_values

    def _choose_action(self, state):
        q_values = self._get_q_values(state)
        action = np.argmax(q_values)
        return action

    def _choose_action_with_exploration(self, state):
        q_values = self._get_q_values(state)
        if np.any(q_values, axis=1):
            if random.random() > 0.8:
                action = np.argmax(q_values)
            else:
                action = self.env.action_space.sample()
        else:
            action = self.env.action_space.sample()
        return action

if __name__ == '__main__':
    agent = Agent()
    for i in range(500):
        agent.train(external_step=i, episodes=50, max_step=200)
        agent.test(delay=0.1, max_step=30)