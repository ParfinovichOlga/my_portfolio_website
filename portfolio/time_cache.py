from functools import lru_cache, wraps
from datetime import datetime, timedelta, timezone

#This func with lru_cache will update cache in a specific period
def timed_lru_cache(days):
    def wrapper_cashe(func):
        func = lru_cache(func)
        func.lifetime = timedelta(days=days)
        func.expiration = datetime.now(timezone.utc) + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now(timezone.utc) >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.now(timezone.utc) + func.lifetime
            return func(*args, **kwargs)  
        return wrapped_func
    return wrapper_cashe  