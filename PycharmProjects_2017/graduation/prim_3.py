import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t = np.linspace(0, 20, 200)
x = np.sin(t)
y = np.cos(t)

ax.scatter(x, y, t)
plt.show()
