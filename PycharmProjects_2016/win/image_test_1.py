import skimage.data, skimage.io, skimage.exposure, skimage.feature
import matplotlib.pyplot as plt
import time


img_1 = skimage.data.coins()
hist_1 = skimage.exposure.histogram(img_1)
edge_1 = skimage.feature.canny(img_1, sigma=2)

img_2 = skimage.exposure.equalize_hist(img_1)
hist_2 = skimage.exposure.histogram(img_2)
edge_2 = skimage.feature.canny(img_2, sigma=2)

img_3 = skimage.exposure.equalize_adapthist(img_1)
hist_3 = skimage.exposure.histogram(img_3)
edge_3 = skimage.feature.canny(img_3, sigma=2)

plt.subplot(331)
plt.imshow(img_1, cmap='gray')
plt.subplot(332)
plt.plot(hist_1[1], hist_1[0])
plt.subplot(333)
plt.imshow(edge_1)
plt.subplot(334)
plt.imshow(img_2, cmap='gray')
plt.subplot(335)
plt.plot(hist_2[1], hist_2[0])
plt.subplot(336)
plt.imshow(edge_2)
plt.subplot(337)
plt.imshow(img_3, cmap='gray')
plt.subplot(338)
plt.plot(hist_3[1], hist_3[0])
plt.subplot(339)
plt.imshow(edge_3)

plt.show()