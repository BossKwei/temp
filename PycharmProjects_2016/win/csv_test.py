import numpy as np
import csv

'''
with open('./test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
'''


m = np.loadtxt(open('test.csv', "rb"),delimiter=",",skiprows=0)
print(m)
print(m.shape)


numpy.loadtxt('odom.txt')


with open('ss15pak.csv', 'r') as f:
    for line in f.readlines():
        print(line.strip())