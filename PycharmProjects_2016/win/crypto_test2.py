import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256



sha = SHA256.new(b'123').hexdigest()

print(len(sha))