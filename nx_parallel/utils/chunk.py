"""Divides an iterable into chunks of size n"""
import itertools
import os

__all__ = ["chunks", "cpu_count"]


def chunks(iterable, n):
    it = iter(iterable)
    while True:
        x = tuple(itertools.islice(it, n))
        if not x:
            return
        yield x


def cpu_count():
    # Check if we are running under pytest
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2
    return os.cpu_count()
