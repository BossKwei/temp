import requests
import random
from threading import Thread

headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
payload = {'idType': '0', 'g_zhanghao': '6221854323459854', 'g_wangyin': '985432', 'g_xingming': '法轮大法', 'g_shouji': '15798543452', 'iaa': '1'}


def make_a_request(): # Make a request
    global headers, payload
    payload['g_zhanghao'] = '6221%d' %random.randint(100000000000, 999999999999)
    payload['g_wangyin'] = '%d' %random.randint(100000, 999999)
    payload['g_shouji'] = '157%d' %random.randint(10000000, 99999999)
    try:
        # r = requests.get('http://wap.cconzm.cc/', params=payload, headers=headers, timeout=(3.05, 8.0))
        r = requests.post('http://wap.ccbqbt.com/post.asp', data=payload, headers=headers, timeout=(3.05, 8.0))
        r.raise_for_status()

        # Print out the response
        print('HTTP Status:', end=' ')
        print(r.status_code, end=' ')
        print(r.reason, end=' ')

        if -1 != r.text.find('lateron.asp'):
            print('Finish')


    except requests.RequestException as e:
        for x in e.args:
            print(x)

def func_proc():
    for i in range(99999999):
        print('%d:' % i, end=' ')
        make_a_request()

if __name__ == '__main__':
    t1 = Thread(target=func_proc, name='loop0')
    t2 = Thread(target=func_proc, name='loop1')
    t3 = Thread(target=func_proc, name='loop2')
    t4 = Thread(target=func_proc, name='loop3')
    t5 = Thread(target=func_proc, name='loop4')

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    func_proc()