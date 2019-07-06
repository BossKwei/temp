import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 5, 50)
y1 = -1.5*x + 5
y2 = -2*x + 5
y3 = 3.15/(x+0.001)

plt.plot(x, y1, x, y2, x, y3)

plt.xlim(0, 5)
plt.ylim(0, 5)

plt.xlabel('public transit')
plt.ylabel('private cars')

plt.show()