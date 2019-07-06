import os
import numpy as np
import scipy.stats
import skimage.io, skimage.color, skimage.morphology, skimage.util
import matplotlib.pyplot as plt


img = skimage.io.imread('/home/bosskwei/Desktop/22.bmp')
skimage.io.imshow(img)
img = skimage.morphology.dilation(img, skimage.morphology.square(3))
skimage.io.imshow(img)
skimage.io.show()