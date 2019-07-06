import time
import threading
import pexpect


class SSHClient(threading.Thread):
    def __init__(self, uri):
        threading.Thread.__init__(self)
        self._process = pexpect.spawn('/usr/bin/ssh',
                                      [uri],
                                      timeout=15.0)
        self._pattern = []

    def run(self):
        while self._process.isalive():
            self._process.expect(self._pattern)

    def login(self, username, password):
        pass
    pexpect.spawn().expect()


def main():
    targets = []
    with open('targets/22.txt', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            line = 'root@' + line
            targets.append(line)
    for t in targets:
        ssh = SSHClient(t)


if __name__ == '__main__':
    main()
