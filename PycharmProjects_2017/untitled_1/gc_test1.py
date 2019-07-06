
class Remote:
    def __init__(self, local):
        self._local = local


class Local:
    def __init__(self):
        self._remote = None

    def data_received(self):
        self._remote = Remote(self)


def func_1():
    local = Local()


class A:
    def __init__(self):
        self.b = None


class B:
    def __init__(self):
        self.a = None


def func_2():
    a = A()
    b = B()
    a.b = b
    b.a = a


if __name__ == '__main__':
    import gc
    func_1()
    print(gc.collect())


