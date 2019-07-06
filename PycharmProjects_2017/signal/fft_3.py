import numpy as np
import matplotlib.pyplot as plt
import scipy, scipy.fftpack, scipy.signal
import pywt


def func_dft(Fs, T, N):
    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 100 * t) + np.sin(
        2 * np.pi * 300 * t)

    yf = scipy.fftpack.fft(y)
    yy = scipy.fftpack.ifft(yf)
    print(np.sum(np.abs(yy - y)) / N)


def func_dct(Fs, T, N):
    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 100 * t) + np.sin(
        2 * np.pi * 300 * t)

    yf = scipy.fftpack.dct(y)
    yy = scipy.fftpack.idct(yf)
    print(np.sum(np.abs(yy - y)) / N)


def func_dst(Fs, T, N):
    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 100 * t) + np.sin(
        2 * np.pi * 300 * t)

    yf = scipy.fftpack.dst(y)
    yy = scipy.fftpack.idst(yf)
    print(np.sum(np.abs(yy - y)) / N)


def func_dwt(Fs, T, N):
    t = np.linspace(0, N * T, N)
    y = np.sin(2 * np.pi * 10 * t) + 0.1 * np.sin(2 * np.pi * 300 * t)

    (cA, cD) = pywt.dwt(y, 'db1')
    yy = pywt.idwt(cA, cD, 'db1')
    print(np.sum(np.abs(yy - y)) / N)


if __name__ == '__main__':
    Fs = 1000
    T = 1 / Fs
    N = 500

    func_dft(Fs, T, N)
    func_dct(Fs, T, N)
    func_dst(Fs, T, N)
    func_dwt(Fs, T, N)

