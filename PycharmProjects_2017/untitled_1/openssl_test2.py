import os
import time
import struct
import ctypes

import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


def encrypt(key, plaintext):
    iv = os.urandom(16)

    encryptor = Cipher(
        algorithms.AES(key),
        modes.CFB(iv),
        backend=default_backend()
    ).encryptor()

    a1 = encryptor.update(plaintext)
    a2 = encryptor.finalize()
    ciphertext = a1 + a2
    return iv, ciphertext


def decrypt(key, iv, ciphertext):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CFB(iv),
        backend=default_backend()
    ).decryptor()

    a1 = decryptor.update(ciphertext)
    a2 = decryptor.finalize()

    return a1 + a2


if __name__ == '__main__':
    time.sleep(10)
    while True:
        key = b'0123456789012345'
        iv, ciphertext = encrypt(key, b"zxcvbnm")
        print(decrypt(key, iv, ciphertext))
