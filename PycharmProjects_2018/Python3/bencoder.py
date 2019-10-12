def encode(x):
    """
    param:
        object, contains int, str, list, dict.
    return:
        bytes, return the bencoded data.
    """
    if type(x) == int:
        return b'i' + str(x).encode() + b'e'
    elif type(x) == bytes:
        return str(len(x)).encode() + b':' + x
    elif type(x) == list:
        end = b'l'
        for i in x:
            end += encode(i)
        end += b'e'
        return end
    elif type(x) == dict:
        keys = list(x.keys())
        # keys = sorted(list(x.keys()))
        end = b'd'
        for i in keys:
            end += encode(i)
            end += encode(x[i])
        end += b'e'
        return end
    else:
        raise TypeError


class Decoder:
    def __init__(self):
        self.idx = 0

    def decode(self, x):
        # int
        if x[self.idx] == ord('i'):
            val = ''
            self.idx += 1
            while x[self.idx] != ord('e'):
                val += str(x[self.idx] - ord('0'))
                self.idx += 1
            self.idx += 1
            return int(val)
        # bytes
        elif ord('0') <= x[self.idx] <= ord('9'):
            val = ''
            while x[self.idx] != ord(':'):
                val += str(x[self.idx] - ord('0'))
                self.idx += 1
            length = int(val)
            self.idx += 1
            res = x[self.idx:self.idx + length]
            self.idx += length
            return res
        # list
        elif x[self.idx] == ord('l'):
            raise NotImplementedError
        # dict
        elif x[self.idx] == ord('d'):
            d = dict()
            self.idx += 1
            while x[self.idx] != ord('e'):
                key = self.decode(x)
                value = self.decode(x)
                d[key] = value
            self.idx += 1
            return d
        else:
            raise NotImplementedError

def decode(x):
    """
    param:
        1. bytes, the bytes will be decode.
        2. str or list, when can not decode with utf-8 charset will try using this charset decoding. 
    return:
        object, unable decoding data will return bytes.
    """ 
    return Decoder().decode(x)
