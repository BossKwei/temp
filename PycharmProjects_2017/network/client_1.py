import time
import struct
import asyncio


class TimeoutHandler:
    def __init__(self):
        self._transport = None
        self._last_active_time = time.time()
        self._timeout_seconds = 10.0

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

    def close(self):
        if self._transport is not None:
            self._transport.close()

    def connection_made(self, transport):
        self._transport = transport
        self.keep_alive_open()
        transport.write(struct.pack('d', time.time()))

    def data_received(self, buffer):
        pass

    def eof_received(self):
        pass

    def connection_lost(self, exc):
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(Client, '127.0.0.1', 8000)
    loop.run_until_complete(coro)
    loop.run_forever()
