import logging
from functools import wraps

logger = logging.getLogger(__name__)

LOGGER_CONFIG = {
    "format": "%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",  # noqa 501
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO,
    "handlers": [logging.StreamHandler()],
}

logging.basicConfig(**LOGGER_CONFIG)


class ETLError(Exception):
    """ETL error class."""

    pass


def backoff(start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10):
    """
    Function for retrying the execution of a function after some time if an error occurs.
    Uses a naive exponential growth of the retry time (factor) up to the maximum waiting time (border_sleep_time).

    Formula:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: initial retry time
    :param factor: how many times to increase the waiting time
    :param border_sleep_time: maximum waiting time
    :return: the result of the function execution.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except ETLError:
                    logger.exception('Error while transferring data')
                    sleep_time = min(sleep_time * 2**factor, border_sleep_time)

        return inner

    return func_wrapper
