import asyncio


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


def cb(future):
    transport, protocol = future.result()
    print('callback')
    print(transport)
    print(protocol)

loop = asyncio.get_event_loop()
message = '1234567890'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', 8888)
task = asyncio.ensure_future(coro)
task.add_done_callback(cb)
# loop.run_until_complete(coro)
loop.run_forever()
loop.close()
