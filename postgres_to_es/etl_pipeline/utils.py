import time
import logging

from functools import wraps


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, exception=Exception):
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост
    времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param exception исключение, которое выбрасывается при неуспешном соединении
    :return: результат выполнения функции
    """
    def calc_break_time(n):
        return start_sleep_time * factor**n

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            break_time = calc_break_time(n)
            while break_time < border_sleep_time:
                try:
                    func(*args, **kwargs)
                    break
                except exception:
                    logging.warning("couldn't establish connection, retry in {}".format(str(break_time)))
                    time.sleep(break_time)
                    n += 1
                    break_time = calc_break_time(n)
        return inner

    return func_wrapper


def establish_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "{asctime}\t{threadName:>11}\t{levelname}\t{message}", style='{')

    # Log to file
    filehandler = logging.FileHandler("debug.txt", "w")
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    log.addHandler(filehandler)

    # Log to stdout too
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(formatter)
    log.addHandler(streamhandler)

    return log
