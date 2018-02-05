import logging, logging.handlers


logging.basicConfig(
                    format='[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s - %(message)s',
                    level=logging.DEBUG)


def xxx():
    logging.info('1')
    logging.debug('2')


xxx()