import numpy as np


def main():
    a(1)


def b(func):
    def _a(p):
        print('b-start')
        func(p)
        print('b-end')
    return _a


@b
def a(p):
    print('a-start')
    print(p)
    print('a-end')


if __name__ == '__main__':
    main()