import os
import pty
import time
import logging


def main():
    pid, fd = pty.fork()
    if pid == 0:
        os.execlp('/usr/bin/ssh', 'ssh', 'root@ss.1415926.science')
        # os.execlp('ls', 'ls -l')
    else:
        while True:
            try:
                status = os.waitpid(pid, os.WNOHANG)  # if child exit immediately, waitpid() could still return one time
                print(status)
                a = os.read(fd, 1024)
                print(a)
            except OSError as e:
                if e.errno == 5:  # [Errno 5] Input/output error
                    pass
                elif e.errno == 10:  # [Errno 10] No child processes
                    break
                else:
                    logging.warning('Unhandled Exception: {0} {1}'.format(type(e), e))
            time.sleep(1)


if __name__ == '__main__':
    main()
