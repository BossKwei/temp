import pywt
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(512)
y = np.sin(2 * np.pi * x / 32)
scales = np.linspace(1, 64, 64)
plt.plot(x, y)
coef, freqs = pywt.cwt(y, scales, 'gaus1')
plt.matshow(coef)

import pywt
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-1, 1, 200, endpoint=False)
sig = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7 * (t - 0.4) ** 2) * np.exp(1j * 2 * np.pi * 2 * (t - 0.4)))
plt.plot(t, sig)
plt.show()
widths = np.arange(1, 31)
cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()
