import time


def wrapper_1(func):
    def wrapper(*args, **kwargs):
        print('wrapper_1')
        return func(*args, **kwargs)
    return wrapper


def wrapper_2(config):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(config)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def wrapper_3(func):
    print('wrapper_3')
    return func


def wrapper_4(config):
    def handler(func):
        print(config)
        return func
    return handler


@wrapper_1
def work_1():
    print('work_1')


@wrapper_2('wrapper_2')
def work_2():
    print('work_2')


@wrapper_3
def work_3():
    print('work_3')


@wrapper_4('wrapper_4')
def work_4():
    print('work_4')


def main():
    print('------------')
    for i in range(3):
        work_1()
    print('------------')
    for i in range(3):
        work_2()
    print('------------')
    for i in range(3):
        work_3()
    print('------------')
    for i in range(3):
        work_4()
    print('------------')


if __name__ == '__main__':
    main()