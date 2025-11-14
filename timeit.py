import time
from functools import wraps
from colorama import Fore
from colorama import Style

def timeit(func, print_args=False):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'{Style.BRIGHT}{func.__name__}{Style.RESET_ALL}' + (f'{args} {kwargs}' if print_args else '') + f' took {Style.BRIGHT}{total_time:.8f}s{Style.RESET_ALL}.')

        return result

    return timeit_wrapper
