import time
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.multiply(np.sin(2 * np.pi * x), np.exp(- np.multiply(x, x)))


def randu(N, lower, higher):
    return np.random.rand(N) * (higher - lower) + lower


def main():
    S = 100
    MIN, MAX = -5, 5
    phi_p, phi_g = 1.0, 1.0
    omega = 0.1
    #
    x = np.array(randu(S, MIN, MAX), dtype=np.float32)
    p = np.array(x, dtype=np.float32)
    g = np.random.choice(x, 1)
    for i in range(S):
        if f(p[i]) < f(g):
            g = p[i]
    v = np.array(randu(S, -np.abs(MAX - MIN), np.abs(MAX - MIN)), dtype=np.float32)
    #
    hx = []
    for step in range(1000):
        for i in range(S):
            r_p, r_g = randu(2, 0, 1)
            v[i] = omega * v[i] + phi_p * r_p * (p[i] - x[i]) + phi_g * r_g * (g - x[i])
            x[i] += v[i]
            #
            if f(x[i]) < f(p[i]):
                p[i] = x[i]
                if f(p[i]) < f(g):
                    g = p[i]
        hx.append(x.copy())
    print(x)
    #
    for x in hx:
        plt.plot(np.linspace(MIN, MAX, 100), f(np.linspace(MIN, MAX, 100)))
        plt.scatter(x, f(x), marker='x')
        plt.show()


if __name__ == '__main__':
    main()
