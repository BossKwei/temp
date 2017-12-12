import numpy as np


buf = list()


def add(*arg):
    print(arg)
    buf.append(arg)

if __name__ == '__main__':
    add(1, 1, 1)
    add(2, 2, 2)
    add(3, 3, 3)
    print(buf)
    print(*buf)
    a, b, c = zip(*buf)
    print(a,b,c)