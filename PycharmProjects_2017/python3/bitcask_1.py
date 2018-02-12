import time
import json
import pathlib
from collections import namedtuple


class DBase:
    DB_PATH = 'db/'
    DB_MAX_ORDINAL = 0xFFFFFFFF
    DB_FORMATTER = namedtuple('DB_FORMATTER', ['stamp', 'key', 'value'])
    DB_MAX_SIZE = 8 * 1024 * 1024
    TABLE_FORMATTER = namedtuple('TABLE_FORMATTER', ['file', 'offset'])

    def __init__(self):
        self._table = dict()

        self._db_path = pathlib.Path(self.DB_PATH)
        if not self._db_path.exists():
            self._db_path.mkdir()
        if not self._db_path.is_dir():
            raise RuntimeError('not a dir DB_PATH: {}'.format(self.DB_PATH))

        self._db_files = list()
        for i in range(self.DB_MAX_ORDINAL):
            child = self._db_path.joinpath('storage.{}.db'.format(i))
            if not child.exists():
                break
            if not child.is_file():
                raise RuntimeError('error file: {}'.format(child))
            self._db_files.append(child.open(mode='r'))
        else:
            raise RuntimeError('out of DB_MAX_ORDINAL: {}'.format(self.DB_MAX_ORDINAL))
        self._num_dbs = len(self._db_files)
        self._active_file = None

    def __del__(self):
        for f in self._db_files:
            f.close()

    def _switch_active_db(self):
        child = self._db_path.joinpath('storage.{}.db'.format(self._num_dbs))
        if child.exists():
            raise RuntimeError('error num_dbs: {}'.format(self._num_dbs))
        writer, reader = child.open(mode='a'), child.open(mode='r')
        self._db_files.append(reader)
        if self._active_file is not None:
            self._active_file.close()
        self._active_file = writer
        self._num_dbs += 1

    def update(self, key, value):
        buffer = self.DB_FORMATTER(stamp=time.time(),
                                   key=key,
                                   value=value)
        if self._active_file is None or self._active_file.tell() > self.DB_MAX_SIZE:
            self._switch_active_db()
        self._table[key] = self.TABLE_FORMATTER(file=self._db_files[-1],
                                                offset=self._active_file.tell())
        print(json.dumps(buffer), end='\n', file=self._active_file, flush=True)

    def get(self, key, default=None):
        if key not in self._table:
            return default
        file, offset = self._table[key]
        file.seek(offset)
        line = file.readline()
        stamp, key, value = json.loads(line)
        return value


def test_db():
    import os
    import random

    db = DBase()
    table = dict()
    #
    before = time.time()
    for i in range(0xFFFFF):
        key = random.randrange(0xFF)
        value = random.randrange(0xFFFFFFFF)
        table[key] = value
        db.update(key, value)
    after = time.time()
    print('Update QPS: {}'.format(0xFFFFF / (after - before)))
    #
    for key in table:
        value = table[key]
        assert value == db.get(key)
    #
    time.sleep(10.0)
    #
    before = time.time()
    for i in range(0xFFFFF):
        key = random.randrange(0xFF)
        db.get(key)
    after = time.time()
    print('Get QPS: {}'.format(0xFFFFF / (after - before)))
    # ----------------------------------
    # Update QPS: 51655.79078981179
    # Get QPS: 23650.67930437536
    # ----------------------------------


if __name__ == '__main__':
    test_db()
