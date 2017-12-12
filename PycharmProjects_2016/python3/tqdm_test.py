from tqdm import tqdm,trange
import time


for i in trange(10):
    if i & 2 == 0:
        tqdm.write('s')
    time.sleep(0.5)