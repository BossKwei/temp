import numpy as np
import matplotlib.pyplot as plt


t = np.matrix([[-1, -1, 0, 2, 0], [-2, 0, 0, 1, 1]])
print(np.linalg.eig(0.2*np.matmul(t, t.T)))

a = np.array([[-1, -2],
              [-1, 0],
              [0, 0],
              [2, 1],
              [0, 1]], dtype=np.float32)

p = np.array([[1/1.414, 1/1.414], [-1/1.414, 1/1.414]], dtype=np.float32)
print(np.linalg.norm(p, ord=1))
a2 = np.matmul(p, a.T)

b = np.cov(a.T)

fig = plt.figure()

ax = fig.add_subplot(1, 2, 1)
ax.set_title('1')
ax.scatter(a.T[0], a.T[1], marker='x')
ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax = fig.add_subplot(1, 2, 2)
ax.set_title('2')
ax.scatter(a2[0], a2[1], marker='x')
ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.show()

print(b)