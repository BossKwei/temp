import multiprocessing as mp

import time
import os


def f(q):
    print('f start')
    q.put(1)
    time.sleep(5)
    q.put(2)
    print('f end')


if __name__ == '__main__':
    print('main start')
    q = mp.Queue()
    p = mp.Process(target=f, args=(q,))
    p.start()
    print(q.get())
    p.join()
    print('main end')