import time
import asyncio
import concurrent.futures
import requests


def func_1(url):
    print('enter:', url)
    response = requests.get(url)
    print(response.headers)
    print('leave:', url)


def main():
    executor = concurrent.futures.ThreadPoolExecutor()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, func_1, 'https://www.taobao.com/')
    loop.run_in_executor(executor,func_1, 'https://www.baidu.com/')
    loop.run_in_executor(executor, func_1, 'https://www.zhihu.com/')
    loop.run_forever()


if __name__ == '__main__':
    main()