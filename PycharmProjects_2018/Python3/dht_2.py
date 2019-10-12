import os
import sqlite3
import logging
import asyncio
import binascii
from socket import inet_ntoa, inet_aton
from struct import unpack
import bencoder


def random_node_id(size=20):
    return os.urandom(size)


def split_nodes(nodes):
    length = len(nodes)
    if (length % 26) != 0:
        return

    for i in range(0, length, 26):
        nid = nodes[i:i + 20]
        ip = inet_ntoa(nodes[i + 20:i + 24])
        port = unpack('!H', nodes[i + 24:i + 26])[0]
        yield nid, ip, port


class DHTServer(asyncio.DatagramProtocol):
    BOOTSTRAP_NODES = (
        ('router.bittorrent.com', 6881),   # 67.215.246.10
        ('dht.transmissionbt.com', 6881),  # 212.129.33.59
        ('router.utorrent.com', 6881)      # 82.221.103.244
    )

    def __init__(self, loop=None, bootstrap_nodes=BOOTSTRAP_NODES, interval=120.0):
        self.node_id = random_node_id()
        self.transport = None
        self.loop = loop or asyncio.get_event_loop()
        self.bootstrap_nodes = bootstrap_nodes
        self.__running = False
        self.interval = interval

    def stop(self):
        self.__running = False
        self.loop.call_later(self.interval, self.loop.stop)

    async def auto_find_nodes(self):
        while self.__running:
            await asyncio.sleep(self.interval)
            for node in self.bootstrap_nodes:
                self.find_node(addr=node)

    def run(self, port=6881):
        coro = self.loop.create_datagram_endpoint(
            lambda: self, local_addr=('0.0.0.0', port)
        )
        transport, _ = self.loop.run_until_complete(coro)

        for node in self.bootstrap_nodes:
            self.find_node(addr=node, node_id=self.node_id)

        self.__running = True
        asyncio.ensure_future(self.auto_find_nodes(), loop=self.loop)
        self.loop.run_forever()
        self.loop.close()

    def datagram_received(self, data, addr):
        try:
            msg = bencoder.bdecode(data)
        except Exception as e:
            logging.warning('bdecode error: {0} {1}'.format(type(e), e))
            return
        try:
            self.handle_message(msg, addr)
        except Exception as e:
            logging.warning('handle_message error: {0} {1}'.format(type(e), e))
            self.send_message(data={
                b't': msg[b't'],
                b'y': b'e',
                b'e': [202, b'Server Error']
            }, addr=addr)
            raise e

    def handle_message(self, msg, addr):
        msg_type = msg.get(b'y', b'e')

        if msg_type == b'e':
            logging.debug('error from {0}'.format(addr))
            return

        if msg_type == b'r':
            # we only send `find_nodes` and `ping`, so only response for them
            logging.debug('response from {0}'.format(addr))
            return self.handle_response(msg, addr=addr)

        if msg_type == b'q':
            logging.debug('query from {0}'.format(addr))
            return self.handle_query(msg, addr=addr)

    def handle_response(self, msg, addr):
        args = msg[b'r']

        if b'nodes' in args:  # `find_node` response
            logging.debug('node {} response find_node'.format(addr))
            for node_id, ip, port in split_nodes(args[b'nodes']):
                self.ping(addr=(ip, port))

        if b'nodes' not in args and b'id' in args:  # `ping` response
            logging.debug('node {} is alive'.format(addr))

        if b'values' in args:
            logging.debug('node {0} response get_peers {1}'.format(addr, args[b'values']))

    def handle_query(self, msg, addr):
        args = msg[b'a']
        node_id = args[b'id']
        query_type = msg[b'q']
        if query_type == b'get_peers':
            infohash = args[b'info_hash']
            token = infohash[:2]
            self.send_message({
                b't': msg[b't'],
                b'y': b'r',
                b'r': {
                    b'id': self.fake_node_id(node_id),
                    b'nodes': b'',
                    b'token': token
                }
            }, addr=addr)
            self.handle_get_peers(infohash, addr)
        elif query_type == b'announce_peer':
            infohash = args[b'info_hash']
            tid = msg[b't']
            self.send_message({
                b't': tid,
                b'y': b'r',
                b'r': {
                    b'id': self.fake_node_id(node_id)
                }
            }, addr=addr)
            peer_addr = [addr[0], addr[1]]
            # if b'port' in args and b'implied_port' in args and :
            try:
                peer_addr[1] = args[b'port']
            except KeyError:
                pass
            self.handle_announce_peer(infohash, addr, peer_addr)
        elif query_type == b'find_node':
            tid = msg[b't']
            self.send_message({
                b't': tid,
                b'y': b'r',
                b'r': {
                    b'id': self.fake_node_id(node_id),
                    b'nodes': b''
                }
            }, addr=addr)
        elif query_type == b'ping':
            self.send_message({
                b't': b'tt',
                b'y': b'r',
                b'r': {
                    b'id': self.fake_node_id(node_id)
                }
            }, addr=addr)

    def ping(self, addr, node_id=None):
        logging.debug('send ping to {}'.format(addr))
        self.send_message({
            b't': b'pg',
            b'y': b'q',
            b'q': b'ping',
            b'a': {
                b'id': self.fake_node_id(node_id)
            }
        }, addr=addr)

    def find_node(self, addr, node_id=None, target=None):
        if not target:
            target = random_node_id()
        self.send_message({
            b't': b'fn',
            b'y': b'q',
            b'q': b'find_node',
            b'a': {
                b'id': self.fake_node_id(node_id),
                b'target': target
            }
        }, addr=addr)

    def get_peers(self, addr, hashinfo, node_id=None):
        self.send_message({
            b't': b'fn',
            b'y': b'q',
            b'q': b'get_peers',
            b'a': {
                b'id': self.fake_node_id(node_id),
                b'info_hash': binascii.unhexlify(hashinfo)
            }
        }, addr=addr)

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.__running = False
        self.transport.close()

    def send_message(self, data, addr):
        data.setdefault(b't', b'tt')
        self.transport.sendto(bencoder.bencode(data), addr)

    def fake_node_id(self, node_id=None):
        if node_id:
            return node_id[:-1] + self.node_id[-1:]
        return self.node_id

    def handle_get_peers(self, infohash, addr):
        raise NotImplementedError

    def handle_announce_peer(self, infohash, addr, peer_addr):
        raise NotImplementedError


def main():
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(funcName)s() - %(message)s')

    class Crawler(DHTServer):
        def __init__(self):
            DHTServer.__init__(self)

        def handle_get_peers(self, infohash, addr):
            logging.debug('addr: {0}, infohash: {1}'.format(addr, infohash))

        def handle_announce_peer(self, infohash, addr, peer_addr):
            logging.info('addr: {0}, infohash: {1}, peer_addr: {2}'.format(addr, infohash, peer_addr))

    crawler = Crawler()
    crawler.run(6881)


if __name__ == '__main__':
    main()
