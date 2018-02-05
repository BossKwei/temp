import time
import random
import logging
import asyncio

num_tasks = 0


class TimeoutHandler:
    def __init__(self):
        self._transport = None
        self._last_active_time = time.time()
        self._timeout_seconds = 10

    def close(self):
        raise NotImplementedError

    def keep_alive_open(self):
        asyncio.ensure_future(self._keep_alive())

    def keep_alive_active(self):
        self._last_active_time = time.time()

    async def _keep_alive(self):
        while self._transport is not None:
            current_time = time.time()
            if (current_time - self._last_active_time) > self._timeout_seconds:
                self.close()
                break
            else:
                if current_time < self._last_active_time:  # system time reset
                    self.keep_alive_active()
                await asyncio.sleep(2)


class Client(asyncio.Protocol, TimeoutHandler):
    def __init__(self):
        asyncio.Protocol.__init__(self)
        TimeoutHandler.__init__(self)
        self._transport = None
        self._peername = None
        # self._logger = None

    def close(self):
        if self._transport is not None:
            self._transport.close()

    def connection_made(self, transport):
        self._transport = transport
        self._peername = self._transport.get_extra_info('peername')
        self.keep_alive_open()
        host = '{0}'.format(self._peername[0]) if self._peername[1] == 80 else '{0}:{1}'.format(self._peername[0], self._peername[1])
        request = ('GET / HTTP/1.1\r\nHost: {0}\r\nConnection: keep-alive\r\n'
                   'Cache-Control: max-age=0\r\nUser-Agent: Mozilla/5.0 (Wind'
                   'ows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like '
                   'Gecko) Chrome/62.0.3202.89 Safari/537.36\r\nAccept: text/'
                   'html,application/xhtml+xml,application/xml;q=0.9,image/we'
                   'bp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate'
                   '\r\nAccept-Language: en;q=0.9\r\n\r\n'.format(host))
        self._transport.write(request.encode())

    def data_received(self, buffer):
        try:
            buffer, _ = buffer.split(b'\r\n\r\n', maxsplit=1)
            header = buffer.split(b'\r\n')
            logging.info('{0} {1}'.format(self._peername, header))
        except ValueError as e:
            logging.warning('{0} {1} {2}'.format(self._peername, e, buffer[0:128]))
        self.close()

    def eof_received(self):
        pass

    def connection_lost(self, exc):
        pass


def target_generator():
    with open('ips.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            host, port = line.split(':')
            yield host, port


async def manager():
    global num_tasks
    loop = asyncio.get_event_loop()
    for host, port in target_generator():
        while num_tasks > 768:
            await asyncio.sleep(5.0)
        num_tasks += 1
        coro = create_connection(loop, host, port)
        asyncio.ensure_future(coro)


async def create_connection(loop, host, port):
    global num_tasks
    coro = loop.create_connection(Client, host, port)
    try:
        await asyncio.wait_for(coro, 20.0)
    except asyncio.TimeoutError:
        pass
    finally:
        num_tasks -= 1


def exception_handler(loop, context):
    exception = context['exception']
    if isinstance(exception, (TimeoutError, ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError)):
        pass
    else:
        print(type(exception), exception)


def main():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    coro = manager()
    asyncio.ensure_future(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()


def init_logging():
    handler = logging.FileHandler(filename='client.log')
    logging.basicConfig(handlers=[handler],
                        format='[%(levelname)s] %(asctime)s - %(process)d - %(name)s - %(funcName)s() - %(message)s',
                        level=logging.INFO)


if __name__ == '__main__':
    init_logging()
    main()
