import numpy as np
import matplotlib.pyplot as plt


Fs = 100
T = 1 / Fs
N = 500
half_N = 250

t = np.linspace(0, np.pi / 4, N)
x1 = np.sin(2 * np.pi * 10 * t)
f1 = np.fft.fft(x1)
# print(f1)
phase = np.angle(f1)
amplitude = np.abs(f1)

for ph, am in zip(phase, amplitude):
    print('%.2f, %.2f' % (ph, am))

# plt.plot(t, x1)
plt.scatter(phase, amplitude)
plt.show()