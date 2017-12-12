import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


rsa = RSA.generate(1024)

private_key = rsa.exportKey()
print(private_key.decode('ascii'))

public_key = rsa.publickey().exportKey()
print(public_key.decode('ascii'))

message = b'0'*100

cipher = PKCS1_v1_5.new(rsa)
data_1 = cipher.encrypt(message)
print(len(data_1))

sentinel = None
data_2 = cipher.decrypt(data_1, sentinel)

print(data_2)

pass