import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster, preprocessing)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors

x_data = [[1, 100], [2, 300], [3, 1000]]
result = preprocessing.StandardScaler().fit_transform(x_data)
print(result)