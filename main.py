import functools
import sys
import time

#
import warnings


def profiled(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        inner.ncalls += 1
        return func(*args, **kwargs)
    inner.ncalls = 0
    return inner
@profiled
def identity(x):
    return x


#Можно вызвать функции только один раз(проверка на вызов функции)
def once(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not inner.called:
            func(*args, **kwargs)
            inner.called = True
    inner.called = False
    return inner
@once
def initial_settings():
    print("Serrt")


#Сохранение результатов вычисления функции
def memoized(func):
    cache = {}
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return inner
@memoized
def ackerman(m, n):
    if not m:
        return n + 1
    elif not n:
        return ackerman(m - 1, 1)
    else:
        return ackerman(m - 1, ackerman(m, n - 1))


def deprecated(func):
    code = func.__code__
    warnings.warn_explicit(
        func.__name__ + " is deprecated.",
        category='DeprecationWarning',
        filename=code.co_filename,
        lineno=code.co_firstlineno + 1
    )
    return func
@deprecated
def identity(x):
    return x


def square(func):
    return lambda x: func(x * x)
def addsome(func):
    return lambda x: func(x + 42)
@square
@addsome
def identity(x):
    return x