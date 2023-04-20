import pickle
from functools import wraps

from storage import AsyncBaseStorage


def cache(storage: AsyncBaseStorage, cache_lifetime: int = 300):
    """
    Function for working with cache from specific storage.
    It will store the data in storage if it was not there, and retrieve it from storage if it was there.

    :param storage: cache storage
    :param cache_lifetime: cache lifetime in seconds
    :return: data from cache or from function execution
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            key = '{0}_{1}_{2}'.format(func.__name__, args, kwargs)

            if data := await storage.retrieve_data(key):
                return pickle.loads(data)

            if data := await func(*args, **kwargs):
                await storage.save_data(key, pickle.dumps(data), cache_lifetime)
                return data

        return inner

    return func_wrapper
