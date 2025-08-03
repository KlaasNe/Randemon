import time
from functools import wraps

def timeit(func, print_args=False):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}' + (f'{args} {kwargs}' if print_args else '') + f' took {total_time:.8f} seconds.')

        return result

    return timeit_wrapper
