import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


x_data = np.linspace(0, 1, 40)
y_data = np.sqrt(1.0 - x_data**2) + (0.1 * np.random.randn(x_data.shape[0]))
plt.scatter(x_data, y_data)


# 隐函数，只计算误差便可
def residuals(p, x, y):
    return p - (x**2 + y**2)


param_init = [10]
param = leastsq(residuals, param_init, args=(x_data, y_data))
print(param)

plt.show()
