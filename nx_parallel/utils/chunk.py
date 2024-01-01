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
