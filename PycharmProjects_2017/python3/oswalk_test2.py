import os
import numpy as np
import scipy.stats
import skimage.io
import matplotlib.pyplot as plt
import time


for root, dirs, files in os.walk('/home/bosskwei/Desktop/data_set', topdown=False):
    for file in files:
        img_raw = skimage.io.imread(root + '/' + file)
        label = int(root[-1])
        time.sleep(0.1)