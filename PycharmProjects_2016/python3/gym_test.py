import gym
import time

env = gym.make('MountainCarContinuous-v0')
env.reset()
for step in range(1000):
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample())  # take a random action
    print(observation, reward, done)
    time.sleep(0.1)