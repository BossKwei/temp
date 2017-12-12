import skimage.data, skimage.io, skimage.exposure, skimage.feature, skimage.filters
import matplotlib.pyplot as plt


src = skimage.data.page()

img_1 = skimage.exposure.equalize_adapthist(src)

img_2 = skimage.feature.canny(img_1)

plt.subplot(311)
plt.imshow(src, cmap='gray')
plt.subplot(312)
plt.imshow(img_1, cmap='gray')
plt.subplot(313)
plt.imshow(img_2, cmap='gray')

plt.show()

