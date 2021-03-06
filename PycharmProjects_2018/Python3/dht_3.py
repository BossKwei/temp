import os
import random
import socket
import bencoder


def test_bencoder():
    # int
    a = 12345
    b = bencoder.encode(a)
    assert(b == b'i12345e')
    c = bencoder.decode(b)
    assert(c == a)

    # bytes
    a = b'abcdefg.1234567890'
    b = bencoder.encode(a)
    assert(b == b'18:abcdefg.1234567890')
    c = bencoder.decode(b)
    assert(c == a)

    # list
    a = [1, b'a']
    b = bencoder.encode(a)
    assert(b == b'li1e1:ae')
    c = bencoder.decode(b)
    assert(c == a)

    # dict
    a = {
        b't': b'pg',
        b'y': b'q',
        b'q': b'ping',
        b'a': {b'id': 1234567890}
    }
    b = bencoder.encode(a)
    assert(b == b'd1:t2:pg1:y1:q1:q4:ping1:ad2:idi1234567890eee')
    c = bencoder.decode(b)
    assert(c == a)

    #
    print('test_bencoder() passed')


def test_bencoder_heavy(n_iter=1):
    def gen_int():
        return random.randrange(0xFFFFFFFF)

    def gen_bytes():
        n = random.randrange(0xFF) + 1
        return os.urandom(n)
    
    def gen_list():
        l = list()
        n = random.randrange(0xF) + 1
        for _ in range(n):
            func = random.choice([gen_int, gen_bytes])
            item = func()
            l.append(item)
        return l

    def gen_dict(depth):
        d = dict()
        n = random.randrange(0xF) + 1
        for _ in range(n):
            if depth == 0:
                func = random.choice([gen_int, gen_bytes])
                key = func()
                func = random.choice([gen_int, gen_bytes, gen_list])
                value = func()
                d[key] = value
            else:
                func = random.choice([gen_int, gen_bytes])
                key = func()
                func = random.choice(
                    [gen_int, gen_bytes, gen_list, lambda: gen_dict(random.randrange(depth))])
                value = func()
                d[key] = value
        return d

    for i in range(n_iter):
        depth = random.randrange(0xF)
        a = gen_dict(depth)
        print('depth: {}, size: {}'.format(depth, len(a)), end=', ')
        b = bencoder.encode(a)
        c = bencoder.decode(b)
        assert(c == a)
        print('step {}: finished'.format(i))

    print('test_bencoder_heavy() passed')


def test_bencoder_secure():
    a = b'abcdefg.1234567890'
    b = b'l19:abcdefg.1234567890i123ee'
    c = bencoder.decode(b)
    print(c)
    assert(c == a)


def main():
    test_bencoder()
    test_bencoder_heavy(1024)
    # test_bencoder_secure()


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
