def countdown(n):
    print('Counting down from ', n)
    while n > 0:
        yield n
        n -= 1


x = countdown(10)
print(x)
print(next(x))
print(next(x))
print(next(x))
