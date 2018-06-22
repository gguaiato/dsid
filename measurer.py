import statistics
import time

from simple_operations_pb2 import StrParam


def call_10_times_with_statistics(func):
    def func_wrapper(*args, **kwargs):
        time_spent = []
        for i in range(10):
            before = time.time()
            func(*args, **kwargs)
            after = time.time()
            time_spent.append((after-before)*1000.0)
        mean = statistics.mean(time_spent)
        stdev = statistics.stdev(time_spent)
        param_str = ''
        if len(args) > 1:
            if isinstance(args[1], StrParam):
                args_print = str(len(args[1].value))
            elif isinstance(args[1], str):
                args_print = str(len(args[1]))
            else:
                args_print = str(args[1]).replace('\n', '')
            param_str = ' with {}'.format(args_print.ljust(20))
        print('Called {} 10 times {} - Mean Time: {} Standard Deviation: {}'.format(
            func.__name__.ljust(30), param_str.ljust(35), str(mean).ljust(20), stdev
        ))
    return func_wrapper
