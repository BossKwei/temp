import time
import numpy as np
import matplotlib.pyplot as plt
import threading


plt.ioff()


def process():
    for i in range(300):
        print(i)
        plt.plot(np.random.rand(10))
        time.sleep(0.1)


def draw():
    plt.draw()
    plt.pause(1.0)


t1 = threading.Thread(target=process)
t2 = threading.Thread(target=draw)

t1.start()
t2.start()

t1.join()
t2.join()
