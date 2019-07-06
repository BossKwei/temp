import time
import random
import requests
import multiprocessing


r = requests.post('http://127.0.0.1:8000/login', data='43uriheefeff')
r.raise_for_status()
print(r.text)

'''
urls = []
for i in range(10000):
    urls.append('http://127.0.0.1:8888/add?a={0}&b={1}'.format(random.randrange(99999), random.randrange(99999)))

before = time.time()
with multiprocessing.Pool(7) as pool:
    pool.map(requests.get, urls)
after = time.time()

print(10000 / (after - before))
'''