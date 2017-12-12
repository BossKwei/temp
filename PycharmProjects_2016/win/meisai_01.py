import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster, preprocessing)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors

csv_data = np.loadtxt(open('ss15hak.csv', "rb"),delimiter=",")
csv_data = preprocessing.StandardScaler().fit_transform(csv_data)
print(csv_data.shape)


def plot_embedding_3d_with_labels(X, y, title=None):
    # 坐标缩放到[0,1]区间
    x_min, x_max = np.min(X,axis=0), np.max(X,axis=0)
    X = (X - x_min) / (x_max - x_min)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlim3d([0, 1])
    ax.set_ylim3d([0, 1])
    ax.set_zlim3d([0, 1])
    cmap = ['b', 'g', 'r', 'c', 'm', 'y']

    for i in range(X.shape[0]):
        ax.scatter(X[i, 0], X[i, 1], X[i, 2], color=cmap[y[i]], marker='.')
        # ax.text(X[i, 0], X[i, 1], X[i, 2], s=str(i), color=(random.random(), random.random(), random.random()))

    if title is not None:
        plt.title(title)


def plot_embedding_3d(X, title=None):
    # 坐标缩放到[0,1]区间
    x_min, x_max = np.min(X,axis=0), np.max(X,axis=0)
    X = (X - x_min) / (x_max - x_min)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlim3d([0, 1])
    ax.set_ylim3d([0, 1])
    ax.set_zlim3d([0, 1])

    for i in range(X.shape[0]):
        ax.scatter(X[i, 0], X[i, 1], X[i, 2], color=np.random.rand(3, 1), marker='.')
        # ax.text(X[i, 0], X[i, 1], X[i, 2], s=str(i), color=(random.random(), random.random(), random.random()))

    if title is not None:
        plt.title(title)


x_pca = decomposition.PCA(n_components=3).fit_transform(csv_data)
result = cluster.KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1, verbose=True).fit_predict(x_pca)
plot_embedding_3d_with_labels(x_pca, result, 'Dimensionality reduction using K-Means')
print(result[0:50])
# plot_embedding_3d(x_pca)
plt.show()
