import numpy as np
import matplotlib.pyplot as plt


N = 50
# system matrix
A = np.array([1])
B = np.array([0])
H = np.array([1])
V = np.array([0])

# covariance
P_priori = np.zeros(N)
P_posteriori = np.zeros(N)
# state space
x_priori = np.zeros(N) # predict
x_posteriori = np.zeros(N) # optimal
# input matrix
U = np.zeros(N)
# process noise
W = np.zeros(N)
# process covariance
Q = 1e-1
# measurement covariance
R = 1e-1
# Kalman Gain
Kg = np.zeros(N)
# measurement space
z = np.zeros(N)
# Innovation or measurement residual
y = np.zeros(N)
# Innovation (or residual) covariance
S = np.zeros(N)


def measure(x):
    # y = 1 * (x + np.random.normal())
    y = np.sin(2 * np.pi * 100 * x)
    return y


for k in range(1, N):
    # 1.predict
    x_priori[k] = A * x_posteriori[k-1] + W[k]
    P_priori[k] = A * P_posteriori[k-1] * A.T + Q
    # 2. measure
    z[k] = measure(k)
    # 3.update
    y[k] = z[k] - H * x_priori[k]
    S[k] = R + H * P_priori[k] * H.T
    Kg[k] = P_priori[k] * H.T / S[k]
    x_posteriori[k] = x_priori[k] + Kg[k] * y[k]
    P_posteriori[k] = (1 - Kg[k] * H) * P_priori[k]
    # 4.optimal result
    pass


t = np.linspace(0, N)
plt.scatter(t, z, c='r')
# plt.plot(t, 1 * t, c='b')
plt.plot(t, x_posteriori, c='g')

plt.show()