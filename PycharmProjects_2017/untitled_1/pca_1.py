import numpy as np
import matplotlib.pyplot as plt
import sklearn.decomposition, sklearn.datasets


x = np.array([[-1, -2],
              [-1, 0],
              [0, 0],
              [2, 1],
              [0, 1]], dtype=np.float32)

cov = np.cov(x.T)
print(cov)

eigvals, eigvecs = np.linalg.eigh(cov)
print(eigvals)

index = np.argsort(eigvals)[::-1]
eigvals = eigvals[index[0]]
eigvecs = eigvecs[index[0]]

print(np.matmul(x, eigvecs.T))