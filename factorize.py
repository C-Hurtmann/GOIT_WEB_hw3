from multiprocessing.pool import Pool
from functools import wraps
import logging
from time import time


def exec_factorize(number: int) -> list[int]:
    """Main process of solving

    Returns:
        list[int]: numbers which could be divided on number without trace
    """
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
def factorize(numbers: tuple):
    result_list = []
    for number in numbers:
        result_list.append(exec_factorize(number))
    return result_list

@timer
def multi_facrorize(numbers: tuple) -> list[list[int]]:
    result_list = []
    pool = Pool()
    result_list = pool.map_async(exec_factorize, numbers).get()
    return result_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    numbers = (128, 255, 99999, 465466, 12316898, 2058068, 10651060)
    print(factorize(numbers) == multi_facrorize(numbers)) # check if results is the same