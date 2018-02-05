import time
import tqdm
import numpy as np

if __name__ == '__main__':
    a1 = ['F', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
    a2 = ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
    a3 = ['F', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']
    a = [a1, a2, a3]
    m, n = 0, 0
    #
    for i in tqdm.tqdm(range(10000000)):
        ca, = np.random.choice(a, 1)
        np.random.shuffle(ca)
        #
        if ca[1] == 'M':
            n += 1
            if ca[0] == 'F':
                m += 1
    print(m/n)
