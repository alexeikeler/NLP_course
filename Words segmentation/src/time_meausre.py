import time
from functools import wraps

def measure_func_time(function_to_measure):
    @wraps(function_to_measure)
    def inner(*args, **kwargs):
        
        ts = time.time()
        result = function_to_measure(*args, **kwargs)
        te = time.time()

        print(f'Function {function_to_measure.__name__} executed in {(te - ts):4f}s')
 
        return result

    return inner
