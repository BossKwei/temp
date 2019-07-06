import numpy as np
import matplotlib.pyplot as plt
import scipy, scipy.fftpack, scipy.signal
import pywt


def func_1():
    Fs = 1000
    T = 1 / Fs
    N = 500

    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t) + 0.1 * np.sin(2 * np.pi * 300 * t)

    (cA, cD) = pywt.dwt(y, 'db1')
    A = pywt.idwt(cA=cA, cD=None, wavelet='db1')
    D = pywt.idwt(cA=None, cD=cD, wavelet='db1')

    plt.subplot(311)
    plt.plot(y)
    plt.subplot(312)
    plt.plot(A)
    plt.subplot(313)
    plt.plot(D)

    plt.show()


def func_2():
    Fs = 5000
    T = 1 / Fs
    N = 2000

    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t)# + 0.1 * np.sin(2 * np.pi * 300 * t)
    y[500:1000] += 0.1 * np.sin(2 * np.pi * 500 * t[500:1000])

    [cA3, cD3, cD2, cD1] = pywt.wavedec(y, wavelet='db1', level=3)
    A3 = pywt.idwt(cA=cA3, cD=None, wavelet='db1')
    D3 = pywt.idwt(cA=None, cD=cD3, wavelet='db1')
    D2 = pywt.idwt(cA=None, cD=cD2, wavelet='db1')
    D1 = pywt.idwt(cA=None, cD=cD1, wavelet='db1')

    plt.subplot(511)
    plt.plot(y)
    plt.subplot(512)
    plt.plot(A3)
    plt.subplot(513)
    plt.plot(D1)
    plt.subplot(514)
    plt.plot(D2)
    plt.subplot(515)
    plt.plot(D3)

    plt.show()


if __name__ == '__main__':
    func_2()