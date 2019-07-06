import time
import logging
import asyncio


class TimeoutHandler:
    def __init__(self):
        self._local_transport = None
        self._last_active_time = time.time()
        self._timeout_seconds = 20

    def close(self):
        raise NotImplementedError

    def keep_alive_open(self):
        asyncio.ensure_future(self._keep_alive())

    def keep_alive_active(self):
        self._last_active_time = time.time()

    async def _keep_alive(self):
        while self._local_transport is not None:
            current_time = time.time()
            if (current_time - self._last_active_time) > self._timeout_seconds:
                self.close()
                break
            else:
                if current_time < self._last_active_time:  # system time reset
                    self.keep_alive_active()
                await asyncio.sleep(1)


class RemoteTCP(asyncio.Protocol, TimeoutHandler):
    def __init__(self, local_transport, buffer):
        asyncio.Protocol.__init__(self)
        TimeoutHandler.__init__(self)
        self._local_transport = local_transport
        self._remote_transport = None
        self._peername = None
        self._headers = dict()
        self._buffer = buffer

    def close(self):
        if self._remote_transport is not None:
            self._remote_transport.close()
        if self._local_transport is not None:
            self._local_transport.close()

    def connection_made(self, transport):
        self.keep_alive_open()
        self._remote_transport = transport
        self._peername = self._remote_transport.get_extra_info('peername')
        self._remote_transport.write(self._buffer)

    def connection_lost(self, exc):
        self.close()

    def eof_received(self):
        pass

    def data_received(self, buffer):
        self.keep_alive_active()
        self._local_transport.write(buffer)
        try:
            response, payload = buffer.split(b'\r\n\r\n', maxsplit=1)
        except ValueError as e:
            logging.warning('{0} {1} {2}'.format(type(e), e, buffer[0:256]))
        return


class LocalTCP(asyncio.Protocol, TimeoutHandler):
    RESPONSE_400 = (b'HTTP/1.1 400 Bad Request\r\n'
                    b'Connection: close\r\n'
                    b'Content-Type: text/html; charset=ISO-8859-1\r\n'
                    b'Content-Length: 0\r\n\r\n')

    def __init__(self):
        asyncio.Protocol.__init__(self)
        TimeoutHandler.__init__(self)
        self._loop = asyncio.get_event_loop()
        self._local_transport = None
        self._remote_transport = None
        self._peername = None
        self._headers = dict()

    def close(self):
        if self._local_transport is not None:
            self._local_transport.close()
        if self._remote_transport is not None:
            self._remote_transport.close()

    def connection_made(self, transport):
        self.keep_alive_open()
        self._local_transport = transport
        self._peername = self._local_transport.get_extra_info('peername')
        pass

    def connection_lost(self, exc):
        self.close()

    def eof_received(self):
        pass

    def data_received(self, buffer):
        self.keep_alive_active()
        #
        try:
            request, payload = buffer.split(b'\r\n\r\n', maxsplit=1)
            request = request.split(b'\r\n')
            request, headers = request[0], request[1:]
            #
            request_type, request_url, request_version = request.split(b' ')
            if request_type == b'GET':
                pass
            elif request_type == b'POST':
                pass
            else:
                self._local_transport.write(self.RESPONSE_400)
                self.close()
                return
            #
            url_scheme, request_url = request_url.split(b'://')
            if url_scheme != b'http':
                self._local_transport.write(self.RESPONSE_400)
                self.close()
                return
            if request_url.find(b'/') > 0:
                if request_url.endswith(b'/'):
                    url_domain = request_url[0:-1]
                    url_path = b'/'
                else:
                    url_domain, url_path = request_url.split(b'/', maxsplit=1)
            else:
                url_domain = request_url
                url_path = b'/'
            request = request_type + b' ' + url_path + b' ' + request_version + b'\r\n'
            #
            if request_version not in (b'HTTP/0.9', b'HTTP/1.0', b'HTTP/1.1'):
                self._local_transport.write(self.RESPONSE_400)
                self.close()
                return
            #
            for item in headers:
                key, value = item.split(b': ')
                self._headers[key] = value
            #
            host = self._headers[b'Host']
            if host.find(b':') > 0:
                host, port = host.split(b':')
            else:
                port = 80
            if host != url_domain:
                self._local_transport.write(self.RESPONSE_400)
                self.close()
                return
            #
            buffer = request + b'\r\n'.join(headers) + b'\r\n\r\n' + payload
            coro = self._loop.create_connection(lambda: RemoteTCP(self._local_transport, buffer), host, port)
            asyncio.ensure_future(coro)
        except ValueError as e:
            self._local_transport.write(self.RESPONSE_400)
            self.close()
            return
        except KeyError as e:
            self._local_transport.write(self.RESPONSE_400)
            self.close()
            return
        return


def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(LocalTCP, '127.0.0.1', 8080)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


def init_logging():
    import logging.handlers
    handler = logging.handlers.TimedRotatingFileHandler(filename='client.log', when='midnight')
    logging.basicConfig(handlers=[handler],
                        format='[%(levelname)s] %(asctime)s - %(process)d - %(name)s - %(funcName)s() - %(message)s',
                        level=logging.INFO)


if __name__ == '__main__':
    init_logging()
    main()
