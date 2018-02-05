class C:
    def __init__(self):
        print('__init__')
        self._param = 1.0

    def __setattr__(self, key, value):
        print('__setattr__(), key: {0}, value:{1}'.format(key, value))

    def __getattr__(self, item):
        print('__getattr__')

    def __call__(self, *args, **kwargs):
        print('__call__')


c = C()
c(1)
