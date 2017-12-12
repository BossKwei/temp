import numpy as np
import csv


with open('./csv_test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        a = map(float, row)
        print(a)

