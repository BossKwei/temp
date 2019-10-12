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
        end = b'd'
        for k, v in x.items():
            end += encode(k)
            end += encode(v)
        end += b'e'
        return end
    else:
        raise TypeError


class Decoder:
    def __init__(self, x):
        self.x = x
        self.idx = 0
        self.size = len(self.x)

    def decode(self):
        if not self.idx < self.size:
            raise ValueError

        # int
        if self.x[self.idx] == ord('i'):
            val = ''
            self.idx += 1
            while self.x[self.idx] != ord('e'):
                val += str(self.x[self.idx] - ord('0'))
                self.idx += 1
            self.idx += 1
            return int(val)
        # bytes
        elif ord('0') <= self.x[self.idx] <= ord('9'):
            val = ''
            while self.x[self.idx] != ord(':'):
                val += str(self.x[self.idx] - ord('0'))
                self.idx += 1
            length = int(val)
            self.idx += 1
            res = self.x[self.idx:self.idx + length]
            self.idx += length
            return res
        # list
        elif self.x[self.idx] == ord('l'):
            l = list()
            self.idx += 1
            while self.x[self.idx] != ord('e'):
                item = self.decode()
                l.append(item)
            self.idx += 1
            return l
        # dict
        elif self.x[self.idx] == ord('d'):
            d = dict()
            self.idx += 1
            while self.x[self.idx] != ord('e'):
                key = self.decode()
                value = self.decode()
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
    return Decoder(x).decode()
