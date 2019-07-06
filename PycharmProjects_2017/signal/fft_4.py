import numpy as np
from skimage import io, transform, morphology
import matplotlib.pyplot as plt


lena = io.imread('lena.jpg', as_grey=True)
mark = io.imread('qr.jpg', as_grey=True)

wl = np.fft.fft2(lena)
wm = np.zeros_like(lena)
wm[0:64, 0:64] = mark
# wm[192:256, 192:256] = np.rot90(mark, 2)

print(wl.shape)
print(wm.shape)

alpha = 0.1
ff = wl + alpha * wm
marked_lena = np.fft.ifft2(ff)
marked_lena = np.real(marked_lena)

plt.figure()
plt.imshow(np.real(wl), cmap='gray')

ff = np.fft.fft2(marked_lena)
mark_restore = np.real(ff - wl)

plt.figure()
plt.imshow(np.real(ff), cmap='gray')
plt.show()