import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get('https://www.baidu.com/')
            print(response.status)
            print(await response.text())
        except Exception as e:
            print(e)
        a = 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())