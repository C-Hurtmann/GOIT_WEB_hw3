from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from functools import wraps
import logging
from time import time


def exec_factorize(number: int) -> list[list[int]]:
    dividables  =[]
    for i in range(1, number + 1):
        if not number % i:
            dividables.append(i)
    return dividables


def timer(func):
    @wraps(func)
    def wrapper(*args):
        timer = time()
        result = func(*args)
        logging.debug(f'{func.__name__} - done in {time() - timer}')
        return result
    return wrapper

@timer
def factorize(*numbers):
    result_list = []
    for number in numbers:
        result_list.append(exec_factorize(number))
    return result_list

@timer
def multi_facrorize(*numbers: int) -> list[list[int]]:
    with ProcessPoolExecutor() as executor:
        result_list = tuple(executor.map(exec_factorize, numbers))
        return result_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    a, b, c, d, e  = factorize(128, 255, 99999, 10651060, 86494264)
    ma, mb, mc, md, me = multi_facrorize(128, 255, 99999, 10651060, 86494264)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
