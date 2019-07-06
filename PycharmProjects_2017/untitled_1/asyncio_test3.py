import time
import asyncio


def test_parallel():
    async def func_1(x):
        print(x)
        await asyncio.sleep(x)

    loop = asyncio.get_event_loop()

    coro1 = func_1(1)
    coro2 = func_1(2)

    start = time.time()
    loop.run_until_complete(asyncio.wait([coro1, coro2]))
    print(time.time() - start)


def test_single_tesk():
    async def func_1(x):
        print(x)
        await asyncio.sleep(x)
        return x + 1

    loop = asyncio.get_event_loop()

    coro1 = func_1(1)

    start = time.time()
    task1 = asyncio.ensure_future(coro1)
    loop.run_until_complete(task1)
    print('finish, future result = ', task1.result())
    print(time.time() - start)


def test_multi_tasks():
    async def func_1(x):
        print(x)
        await asyncio.sleep(x)
        return x + 1

    def callback(future):
        print('finish, future result = ', future.result())

    loop = asyncio.get_event_loop()

    coro1 = func_1(1)
    coro2 = func_1(2)

    start = time.time()
    task1 = asyncio.ensure_future(coro1)
    task1.add_done_callback(callback)
    task2 = asyncio.ensure_future(coro2)
    task2.add_done_callback(callback)
    loop.run_until_complete(asyncio.wait([task1, task2]))
    print(time.time() - start)


if __name__ == '__main__':
    test_multi_tasks()