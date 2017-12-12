import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection, cluster)
import random
import matplotlib.cm as cmx
import matplotlib.colors as colors

def plot_embedding_3d(x, y, z, title=None):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlim3d([0, 1])
    ax.set_ylim3d([0, 1])
    ax.set_zlim3d([0, 1])

    for i in range(X.shape[0]):
        ax.scatter(x, y, z, color=np.random.rand(3, 1), marker='o')

    if title is not None:
        plt.title(title)
