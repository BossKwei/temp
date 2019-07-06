import pickle
import plyvel


class LevelDB:
    def __init__(self, path):
        self._db = plyvel.DB(path,
                             create_if_missing=True)
        self._cache = dict()

    def __del__(self):
        self._db.close()

    def __contains__(self, key):
        key = pickle.dumps(key)
        if key in self._cache:
            return True
        value = self._db.get(key, default=None, verify_checksums=False, fill_cache=True)
        return False if value is None else True

    def __getitem__(self, key):
        key = pickle.dumps(key)
        if key in self._cache:
            return self._cache[key]
        value = self._db.get(key, default=None, verify_checksums=True, fill_cache=True)
        if value is None:
            raise KeyError
        return pickle.loads(value)

    def __setitem__(self, key, value):
        key = pickle.dumps(key)
        value = pickle.dumps(value)
        self._cache[key] = value

    def __delitem__(self, key):
        if key in self._cache:
            del self._cache[key]

    def transaction(self):
        pass


def wb_feature():
    db = plyvel.DB('test', create_if_missing=True)
    #
    db.put(b'a', b'-')
    with db.write_batch(transaction=True, sync=False) as wb:
        wb.put(b'a', b'1')
        print(db.get(b'a'))
        wb.put(b'a', b'11')
        print(db.get(b'a'))
    print(db.get(b'a'))
    #
    db.close()


def tx_feature():
    db = LevelDB('test')

    db['a'] = '-'
    with db.transaction() as tx:
        tx['a'] = '1'
        assert db['a'] == '-'
        tx['a'] = '11'
        assert db['a'] == '-'
    assert db['a'] == '11'


def tx_crash_feature():
    db = LevelDB('test')

    db['a'] = '-'
    try:
        with db.transaction() as tx:
            tx['a'] = '1'
            assert db['a'] == '-'
            tx['a'] = '11'
            assert db['a'] == '-'
            raise RuntimeError
    except Exception as _:
        pass
    finally:
        assert db['a'] == '-'


def main():
    # 原始封装
    tx_feature()
    tx_crash_feature()


if __name__ == '__main__':
    main()
