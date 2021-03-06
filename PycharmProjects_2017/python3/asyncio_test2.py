import time
import asyncio
import pyto


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


loop = asyncio.get_event_loop()
#
coro_1 = loop.create_connection(lambda: EchoClientProtocol('1', loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro_1)
#
coro_2 = loop.create_connection(lambda: EchoClientProtocol('2', loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro_2)
#
loop.run_forever()
loop.close()
