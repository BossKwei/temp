import numpy as np
import matplotlib.pyplot as plt


# fft 频谱分析
def func_1():
    Fs = 1000
    T = 1 / Fs
    N = 200

    # sample data
    t = np.linspace(0, N * T, N)
    y1 = np.sin(2 * np.pi * 50 * t)
    y2 = np.cos(2 * np.pi * 150 * t)
    y3 = np.sin(2 * np.pi * 300 * t)
    # transform data
    yf1= np.fft.fft(y1)
    yf2 = np.fft.fft(y2)
    yf3 = np.fft.fft(y3)

    # analyse data
    frequency = np.linspace(0.0, 0.5 * Fs, N // 2)

    def get_amplitude(yf):
        amplitude = np.abs(yf)[0:N // 2] * 2.0 / N
        amplitude[0] = np.real(yf[0]) / N
        return amplitude

    plt.figure()
    plt.subplot(321)
    plt.plot(t, y1)
    plt.subplot(322)
    plt.plot(frequency, get_amplitude(yf1))

    plt.subplot(323)
    plt.plot(t, y2)
    plt.subplot(324)
    plt.plot(frequency, get_amplitude(yf2))

    plt.subplot(325)
    plt.plot(t, y2)
    plt.subplot(326)
    plt.plot(frequency, get_amplitude(yf3))

    plt.show()


# 测试 fftshift 效果
def func_2():
    Fs = 1000
    T = 1 / Fs
    N = 200

    t = np.linspace(0, N * T, N)
    y = np.cos(2 * np.pi * 50 * t)

    frequency1 = np.linspace(0.0, Fs, N)
    yf1 = np.fft.fft(y)
    frequency2 = np.linspace(-Fs / 2, Fs / 2, N)
    yf2 = np.fft.fftshift(yf1)

    plt.figure()
    plt.subplot(121)
    plt.plot(frequency1, 2.0 / N * np.abs(yf1))
    plt.subplot(122)
    plt.plot(frequency2, 2.0 / N * np.abs(yf2))
    plt.show()


# 测试 fftshift 2d 效果
def func_3():
    a = np.array([1, 2, 3, 4, 5])
    b = np.fft.fftshift(a)
    c = np.array([[11, 12, 13],
                  [21, 22, 23],
                  [31, 32, 33]])
    d = np.fft.fftshift(c)
    print(b)
    print(d)


# fft 和 卷积
def func_4():
    Fs = 1000
    T = 1 / Fs
    N = 200

    # sample data
    t = np.linspace(0, N * T, N)
    # y = np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 150 * t) + np.sin(2 * np.pi * 300 * t)
    RC  = 0.01
    y = np.exp(-t / RC) / RC
    frequency = np.linspace(0.0, 0.5 * Fs, N // 2)
    yf = np.fft.fft(y)

    plt.plot(frequency, 2.0 / N * np.abs(yf)[0:N // 2])
    plt.show()


if __name__ == '__main__':
    func_4()