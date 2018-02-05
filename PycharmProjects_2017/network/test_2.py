import random
import time
import threading


class A(threading.Thread):
    def run(self):
        time.sleep(random.randrange(5))


if __name__ == '__main__':
    a = dict()
    try:
        b = a['a']
    except KeyError as e:
        pass
    a = threading.active_count()
    print(a)
    tasks = []
    for i in range(10):
        t = A()
        tasks.append(t)
    for t in tasks:
        t.start()
    while True:
        a = threading.active_count()
        b = threading.enumerate()
        print(b)
        time.sleep(1.0)
