import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


x_data = np.array([1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900], dtype=np.float32)
y_data = np.array([3.9, 5.3, 7.2, 9.6, 12.9, 17.1, 23.2, 31.4, 38.6, 50.2, 62.9, 76.0], dtype=np.float32)
plt.scatter(x_data, y_data)


def func(p, x):
    x0, r = p
    f = x0 * np.exp(r * x)
    return f


def residuals(p, x, y):
    return func(p, x) - y


param_init = [100, 0.01]
param = leastsq(residuals, param_init, args=(x_data, y_data))
print(param)

plt.plot(x_data, func(param[0], x_data))
plt.show()