import time
import asyncio


class EchoServerClientProtocol(asyncio.Protocol):
    def __init__(self):
        print('__init__()')
        self.transport = None
        self.A = 0

    def __del__(self):
        print('__del__()')
        print(self.A)

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self, exc):
        print('connection_lost')

    def eof_received(self):
        print('eof')

    async def another_work(self, x):
        # await asyncio.sleep(5)
        print('another_work() done ', x)

    def data_received(self, data):
        print('data_received()')

        def call_back(future):
            self.A = 9
            print('call_back()')

        task = asyncio.ensure_future(self.another_work(1))
        task = asyncio.ensure_future(self.another_work(2))
        task = asyncio.ensure_future(self.another_work(3))
        task = asyncio.ensure_future(self.another_work(4))
        task = asyncio.ensure_future(self.another_work(5))
        task = asyncio.ensure_future(self.another_work(6))
        task = asyncio.ensure_future(self.another_work(7))
        # task.add_done_callback( call_back )


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
