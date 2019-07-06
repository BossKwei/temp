#! /usr/bin/python3
import os
import time
import json
import ctypes
import random


class RocksDB:
    def __init__(self, path, create_if_missing=True):
        self._wrapper = ctypes.CDLL('./build/libwrapper.so')
        self._instance_id = self._wrapper.rocksdb_open(path.encode('utf-8'), create_if_missing)

    def __del__(self):
        self._wrapper.rocksdb_close(self._instance_id)

    def __contains__(self, key):
        value = self.__getitem__(key)
        if value is None:
            return False
        return True

    def __setitem__(self, key, value):
        key = json.dumps(key).encode('utf-8')
        value = json.dumps(value).encode('utf-8')
        self._wrapper.rocksdb_tx_set(self._instance_id, key, value)

    def __getitem__(self, key):
        key = json.dumps(key).encode('utf-8')
        result_size = self._wrapper.rocksdb_tx_get(self._instance_id, key, None)
        if result_size == 0:
            return None
        result_byte = ctypes.create_string_buffer(result_size)
        self._wrapper.rocksdb_tx_get(self._instance_id, key, result_byte)
        return json.loads(result_byte.value.decode('utf-8'))

    def commit(self):
        self._wrapper.rocksdb_tx_commit(self._instance_id)

    def rollback(self):
        self._wrapper.rocksdb_tx_rollback(self._instance_id)


def main():
    table = dict()
    rocksdb = RocksDB('tmp_db')
    COUNT = 0x7FFFF

    before = time.time()
    for i in range(COUNT):
        key = random.randrange(0xFFFF)
        value = str(os.urandom(64 + random.randrange(8192 - 64)))
        table[key] = value
        rocksdb[key] = value
        if i % 1000 == 999:
            print('\r{:.2f}%'.format(100 * i / COUNT), end='')
            rocksdb.commit()
    rocksdb.commit()
    after = time.time()
    print('{:.2f} writes/sec'.format(COUNT / (after - before)))

    before = time.time()
    for key, value in table.items():
        if value != rocksdb[key]:
            print(value, rocksdb[key])
            raise RuntimeError
    after = time.time()
    print('{:.2f} reads/sec'.format(len(table) / (after - before)))


if __name__ == "__main__":
    main()
