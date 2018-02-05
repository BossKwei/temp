import numpy as np
import matplotlib.pyplot as plt


f = [1, 1, 1, 1, 1, 1, 1, 1, 1]
g = [0, 0.5, 1, 0.5, 0]

for i in range(10):
    h = np.convolve(f, g, 'same')
    print(h)
    f = h

plt.show()