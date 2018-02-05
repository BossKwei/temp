import time
import numpy as np
import tensorflow as tf
import gym
import random
from collections import deque
import time


def show():
    env = gym.make('FrozenLake-v0')
    env.reset()
    env.render()
    s = env.step(0)
    env.render()
    s = env.step(1)
    env.render()
    s = env.step(2)
    env.render()
    print(env.action_space)
    print(env.observation_space)


def choose_action(Q, state):
    actions = Q[state, :]
    if np.any(actions):
        # lead into probability factors
        return np.argmax(actions) if np.random.uniform() < 0.8 else np.random.randint(0, 4)
    else:
        # actions is enpty, so choose a random action
        return np.random.randint(0, 4)


def main():
    #
    env = gym.make('FrozenLake-v0')
    NUM_EPISODES = 5000
    MAX_STEPS = 500
    #
    Q = np.zeros([16, 4], dtype=np.float32)
    lr = 0.1 # learning rate
    df = 0.9 # discount factor
    #
    for episode in range(NUM_EPISODES):
        state = env.reset()
        for step in range(MAX_STEPS):
            # choose action based on current q_table
            action = choose_action(Q, state)
            # apply action and then get reward
            state_, reward, done, info = env.step(action)
            #
            q_target = reward if done else reward + df * np.max(Q[state_, :])
            q_current = Q[state, action]
            Q[state, action] += lr * (q_target - q_current)
            #
            state = state_
            #
            if done:
                break

    print(Q)

    for episode in range(1):
        state = env.reset()
        for step in range(1000):
            action = np.argmax(Q[state, :])
            state_, reward, done, info = env.step(action)  # take a random action
            env.render()
            state = state_
            if done:
                break
            time.sleep(1)


if __name__ == '__main__':
    # show()
    main()