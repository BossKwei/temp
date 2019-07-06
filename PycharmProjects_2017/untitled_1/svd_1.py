import numpy as np
import skimage.data
import matplotlib.pyplot as plt


x1 = skimage.data.page()

u, s, v = np.linalg.svd(x1, full_matrices=False)

print(u.shape)
print(s.shape)
print(v.shape)

s = np.diag(s)

x2 = np.matmul(np.matmul(u, s), v)