import time
import asyncio


def ensure_future_test():
    async def func_1(x):
        print("func_1() start x = ", x)
        asyncio.ensure_future(func_2(x))
        print("func_1() end x = ", x + 1)

    async def func_2(x):
        print("func_2() start x = ", x)
        await asyncio.sleep(10)
        print("func_2() end x = ", x + 2)

    loop = asyncio.get_event_loop()
    coro = func_1(1)
    task = asyncio.ensure_future(coro)
    loop.run_until_complete(task)
    loop.run_forever()


def call_soon_test():
    async def func_1(x):
        print("func_1() start x = ", x)
        loop = asyncio.get_event_loop()
        loop.call_soon(lambda: func_3(x))
        print("func_1() end x = ", x + 1)

    async def func_2(x):
        print("func_2() start x = ", x)
        await asyncio.sleep(10)
        print("func_2() end x = ", x + 2)

    def func_3(x):
        print("func_3() start x = ", x)
        time.sleep(1)
        print("func_3() end x = ", x + 3)

    loop = asyncio.get_event_loop()
    coro = func_1(1)
    task = asyncio.ensure_future(coro)
    loop.run_until_complete(task)
    loop.run_forever()


def ensure_future_tith_time_delay_test():
    async def func_1(x):
        print("func_1() start x = ", x)
        task = asyncio.ensure_future(func_2(x))
        print("func_1() end x = ", x + 1)

    async def func_2(x):
        print("func_2() start x = ", x)
        asyncio.sleep(3)
        print("func_2() end x = ", x + 2)

    loop = asyncio.get_event_loop()
    coro = func_1(1)
    task = asyncio.ensure_future(coro)
    loop.run_forever()


if __name__ == '__main__':
    ensure_future_tith_time_delay_test()
