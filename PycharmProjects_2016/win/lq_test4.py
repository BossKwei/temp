import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import pylab


x_data = np.array([5.31000000000000, 4.50000000000000, 3.61000000000000, 2.21000000000000, 0.420000000000000, -0.240000000000000, -0.790000000000000, -1.03000000000000, -1.07000000000000, -0.960000000000000])
y_data = np.array([87.8800000000000, 87.8800000000000, 86, 79.6200000000000, 65.5900000000000, 55.8300000000000, 38.7900000000000, 27.4900000000000, 20.9700000000000, 11.0200000000000])
plt.scatter(x_data, y_data)


# 隐函数，只计算误差便可
def residuals(p, x, y):
    return p - (x**2 + y**2)


param_init = [10]
param = leastsq(residuals, param_init, args=(x_data, y_data))
print(param)

plt.contour
plt.show()