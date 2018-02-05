class A:
    def __init__(self):
        print('A')
        self.foo()

    def foo(self):
        print('A-foo')


class B(A):
    def __init__(self):
        super().__init__()
        print('B')

    def foo(self):
        print('B-foo')

b = B()