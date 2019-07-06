import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster, preprocessing)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors

# 一年工作小时
def deal_WKW_73(line):
    if line[10] == 1:
        line[10] = 51
    elif line[10] == 2:
        line[10] = 48.5
    elif line[10] == 3:
        line[10] = 43.5
    elif line[10] == 4:
        line[10] = 33
    elif line[10] == 5:
        line[10] = 20
    elif line[10] == 6:
        line[10] = 7
    else:
        print('error')
    #
    line[9] = line[9] * line[10]
    return line[0:10]

# 只计算有工作能力的人
def filter_invalid_row(input_data):
    output_data = []
    for i in range(input_data.shape[0]):
        line = input_data[i]
        find_result = np.argwhere(line == -1.0)
        if find_result.shape[0] == 0:
            line = deal_WKW_73(line)
            output_data.append(line)
    return np.array(output_data)


csv_raw_data = np.loadtxt(open('ss15pusa.csv', 'rb'), delimiter=',', skiprows=1)
#######################################
mask = list(range(1048576))
random.shuffle(mask)
#######################################
sampled_data = csv_raw_data[mask[0:20000]]
print(sampled_data.shape)
filtered_data = filter_invalid_row(sampled_data)
print(filtered_data.shape)