import time
import logging
import asyncio


STAGE_DESTROYED = -1
STAGE_INIT = 0
STAGE_ADDR = 1
STAGE_UDP_ASSOC = 2
STAGE_DNS = 3
STAGE_CONNECTING = 4
STAGE_STREAM = 5


class Remote(asyncio.Protocol):
    def __init__(self, local_transport, data):
        self.local_transport = local_transport
        self.remote_transport = None
        self.data = data

    def connection_made(self, transport):
        print('Remote.connection_made()')
        self.remote_transport = transport
        self.remote_transport.write(self.data)

    def connection_lost(self, exc):
        print('Remote.connection_lost(): exc={exc}'.format(exc=exc))

    def data_received(self, data):
        print('Remote.data_received(): len={len}, data={data}'.format(len=len(data), data=data))
        self.local_transport.write(data)

    def eof_received(self):
        print('Remote.eof_received()')
        self.local_transport.write_eof()


class Local(asyncio.Protocol):
    def __init__(self):
        self.local_transport = None

    def connection_made(self, transport):
        print('Local.connection_made()')
        self.local_transport = transport

    def connection_lost(self, exc):
        print('Local.connection_lost(): exc={exc}'.format(exc=exc))

    def data_received(self, data):
        print('Local.data_received(): len={len}, data={data}'.format(len=len(data), data=data))
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: Remote(self.local_transport, data), 'www.qq.com', 80)
        asyncio.ensure_future(coro)

    def eof_received(self):
        print('Local.eof_received()')


loop = asyncio.get_event_loop()
coro = loop.create_server(Local, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()