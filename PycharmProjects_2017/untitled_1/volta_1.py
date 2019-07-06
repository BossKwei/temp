import numpy as np
import matplotlib.pyplot as plt


def frequency_analysis(t, y, Fs, N):
    assert len(t) == len(y)

    frequency = np.linspace(0.0, 0.5 * Fs, N // 2)
    yf = np.fft.fft(y)

    def get_amplitude(yf):
        amplitude = np.abs(yf)[0:N // 2] * 2.0 / N
        amplitude[0] = np.real(yf[0]) / N
        return amplitude

    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(8, 4))
    ax1.plot(t, y)
    ax2.plot(frequency, get_amplitude(yf))


def main():
    print(np.sqrt(5))
    #
    t1 = np.linspace(0, 2 * np.pi / 100, 65536, dtype=np.float32)
    t2 = np.linspace(0, 2 * np.pi / 200, 65536, dtype=np.float32)
    # t3 = np.linspace(0, 2 * np.pi / 100, 655, dtype=np.float32)
    x1 = 3.0 * np.sin(100 * t1)
    x2 = 4.0 * np.cos(200 * t2)
    x3 = 3.0 * np.sin(100 * t1) + 4.0 * np.cos(200 * t1)
    #
    print(np.sum(np.abs(x1)))
    print(np.sum(np.abs(x2)))
    print(np.sum(np.abs(x3)))
    #
    frequency_analysis(t1, x1, 1 / 65536, 65536)
    frequency_analysis(t2, x2, 1 / 65536, 65536)
    frequency_analysis(t1, x3, 1 / 64, 65536)
    plt.show()


if __name__ == '__main__':
    main()
