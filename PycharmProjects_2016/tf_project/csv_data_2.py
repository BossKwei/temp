import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster, preprocessing)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors


with open('/media/bosskwei/Work/us_data/ss15pusa.csv', 'rb') as f:
    i = 0
    for line in f.readlines():
        print(line.strip())
        i += 1
        break