import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster, preprocessing)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors


def l2_distance(x1, x2):
    return np.sqrt((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2)

X_DATA = np.array([[1, 0], [-1, 0], [2, 0], [-2, 0]])
km = cluster.KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1, verbose=True).fit(X_DATA)
print(km.cluster_centers_)
print(km.inertia_)


'''
km = cluster.KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1, verbose=True).fit(X_DATA)
print(km.labels_)
print('')
print(km.cluster_centers_)
#r = km.fit_predict(X_DATA)
'''