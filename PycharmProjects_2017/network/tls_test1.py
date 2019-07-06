import ssl
import asyncio


class EchoServerClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self, exc):
        print('connection_lost')

    def eof_received(self):
        print('eof')

    def data_received(self, data):
        print('data_received()')


def main():
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('ss.crt', 'ss.key')

    loop = asyncio.get_event_loop()
    coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 888, ssl=ssl_context)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()