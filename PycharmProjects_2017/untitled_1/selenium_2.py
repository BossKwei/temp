import time
import re
import threading
from selenium import webdriver


class Browser(threading.Thread):
    STAGE_INIT = 0x00
    STAGE_0001 = 0x01
    STAGE_HOLD = 0xFF

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print(self.name)
        time.sleep(5)


if __name__ == '__main__':
    Browser().start()
    Browser().start()
    time.sleep(1)
