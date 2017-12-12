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


csv_raw_data = np.loadtxt(open('ss15pak.csv', 'rb'), delimiter=',', skiprows=1,  usecols=[7, 10, 58, 59, 61, 64, 65, 66, 69, 70, 72]) # used col - flag
filtered_data = filter_invalid_row(csv_raw_data)
print(filtered_data.shape)


def plot_embedding_3d_with_labels(X, y=None, title=None):
    X = preprocessing.MinMaxScaler().fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlim3d([0, 1])
    ax.set_ylim3d([0, 1])
    ax.set_zlim3d([0, 1])
    # cmap = ['b', 'g', 'r', 'c', 'm', 'y']
    cmap = np.random.rand(20, 3, 1)

    if y is not None:
        counts = np.bincount(y)
        most_common_y = np.argmax(counts)
        cmap[most_common_y] = [0xf0,0xff,0xff]
        #
        for i in range(X.shape[0]):
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color=cmap[y[i]], marker='.')
    else:
        for i in range(X.shape[0]):
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color=np.random.rand(3, 1), marker='.')

    if title is not None:
        plt.title(title)


def plot_embedding_2d_with_labels(X, y=None, title=None):
    X = preprocessing.MinMaxScaler().fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    # cmap = ['b', 'g', 'r', 'c', 'm', 'y']
    cmap = np.random.rand(20, 3, 1)

    if y is not None:
        for i in range(X.shape[0]):
            ax.scatter(X[i, 0], X[i, 1], color=cmap[y[i]], marker='o')
    else:
        for i in range(X.shape[0]):
            ax.scatter(X[i, 0], X[i, 1], color=np.random.rand(3, 1), marker='o')

    if title is not None:
        plt.title(title)


preprocessed_data = preprocessing.StandardScaler().fit_transform(filtered_data)
x_pca = decomposition.PCA(n_components=3).fit_transform(preprocessed_data)
# plot_embedding_3d_with_labels(x_pca)
# result_label = cluster.KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1, verbose=True).fit_predict(preprocessed_data)
result_label = cluster.MeanShift().fit_predict(preprocessed_data)
plot_embedding_3d_with_labels(x_pca, result_label)

plt.show()