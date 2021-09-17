from functools import wraps
from time      import perf_counter as prf_cnt #코드 실행시간 측정

from django.db   import connection, reset_queries
from django.conf import settings

def query_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start                   = prf_cnt()
        result                  = func(*args, **kwargs)
        end                     = prf_cnt()
        number_of_end_queries   = len(connection.queries)
        print("========================================")
        print(f"function : {func.__name__}")
        print(f"number of queries : {number_of_end_queries - number_of_start_queries}")
        print(f"finished in : {(end - start):.2f}s")
        return result
    return wrapper
