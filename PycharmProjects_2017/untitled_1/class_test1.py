class Local():
    def __init__(self):
        pass

    def __repr__(self):
        return '<%s(127.0.0.1: 8000) %s %s>' % (
            self.__class__.__name__,
            self.__class__.__module__,
            hex(id(self))
        )

    def test(self):
        print(self)


l = Local()
l.test()
