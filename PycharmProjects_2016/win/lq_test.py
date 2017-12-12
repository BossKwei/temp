import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


x_data = np.linspace(0, 10, 20)
y_data = 1.0 * x_data + 1.0 + (0.1 * np.random.randn(x_data.shape[0]))
plt.scatter(x_data, y_data)


def func(p, x):
    k, b = p
    f = k * x + b
    return f


def residuals(p, x, y):
    return func(p, x) - y


param_init = [100 ,100]
param = leastsq(residuals, param_init, args=(x_data, y_data))
print(param)

plt.plot(x_data, func(param[0], x_data))
plt.show()

'''
def func(p, x):
    a, b = p
    y_ = (b*b*(1 - (x*x)/(a*a)))
    return y_*y_


def error(p, x, y, s):
    return func(p, x) - y

#TEST
p0 = [1, 1]

Para = leastsq(error, p0, args=(Xi*Xi, Yi*Yi)) #把error函数中除了p以外的参数打包到args中
print(Para)

plt.scatter(Xi, Yi, label="Sample Point") #画样本点

x=np.linspace(Xi.min(), Xi.max(), 1000)
y=func(Para[0], x)
plt.plot(x, y, label="Fitting Line") #画拟合直线
#plt.legend()
plt.show()
'''