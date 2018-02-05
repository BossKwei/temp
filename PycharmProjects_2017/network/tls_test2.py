import ssl
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


ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)


loop = asyncio.get_event_loop()
message = '1234567890'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              'yun.1415926.science', 22, ssl=ssl_context)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
