import logging
from functools import wraps
from logging import config as logging_config

from .logger import LOGGING

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING)


def backoff(
    expected_exception: type[Exception],
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
):
    """
    Function for retrying the execution of a function after some time if an error occurs.
    Uses a naive exponential growth of the retry time (factor) up to the maximum waiting time (border_sleep_time).

    Formula:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    :param expected_exception: expected exception to backoff
    :param start_sleep_time: initial retry time
    :param factor: how many times to increase the waiting time
    :param border_sleep_time: maximum waiting time

    :return: the result of the function execution.
    """

    def func_wrapper(func: callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return await func(*args, **kwargs)
                except expected_exception:  # noqa
                    sleep_time = min(sleep_time * 2**factor, border_sleep_time)
                    logger.exception('Connection error, retrying in %s s', sleep_time)

        return inner

    return func_wrapper
