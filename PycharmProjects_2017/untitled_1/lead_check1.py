import re


f = open('C:/Users/Mr.Trojan/Desktop/1.txt')

a = dict()
c = 0
d = 0

for l in f.readlines():
    if l.find('construct') != -1:
        c += 1
    elif l.find('destruct') != -1:
        d += 1

print(c)
print(d)