import numpy as np


x = np.array([1, 2, 3], dtype=np.float32)
print(x)

x1 = x[:, np.newaxis]
print(x1)

x2 = x[np.newaxis, :]
print(x2)

x3 = x[np.newaxis, :, np.newaxis]
print(x3)