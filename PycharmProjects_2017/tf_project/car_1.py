import time
import random
import numpy as np
import tensorflow as tf
import gym


env = gym.make('CarRacing-v0')
env.reset()
while True:
    action = env.action_space.sample()
    state_, reward, done, _ = env.step(action)
    env.render()
    print(state_.shape, reward, done)
