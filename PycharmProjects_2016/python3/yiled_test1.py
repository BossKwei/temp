
def yield_test(n):
    i = 0
    while i < n:
        yield i
        i += 1


def yield_test2(x):
    yield from range(x, 0, -1)
    yield from range(x)
    yield from yield_test(3)


if __name__ == '__main__':
    #
    for a in yield_test(5):
        print(a)
    #
    f = yield_test(5)
    for _ in range(5):
        a = next(f)
        print(a)
    #
    print('--------------')
    for i in yield_test2(5):
        print(i)