import random


def rand():
    seed = random.randint(0, 65535)
    while True:
        seed = seed * 6364136223846793005 + 1
        seed = seed % 0xFF
        yield seed


if __name__ == '__main__':
    i = range(1, 10)
    i = list(i)
    random.shuffle(i)
    print(i)