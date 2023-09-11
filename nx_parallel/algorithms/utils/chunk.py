import itertools

"""Divides an iterable into chunks of size n"""
def chunks(l, n):
    l_c = iter(l)
    while True:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x