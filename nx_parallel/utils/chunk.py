import itertools
import os

__all__ = ["chunks", "cpu_count"]


def chunks(iterable, n):
    """Divides an iterable into chunks of size n"""
    it = iter(iterable)
    while True:
        x = tuple(itertools.islice(it, n))
        if not x:
            return
        yield x


def cpu_count(n_jobs=-1):
    """Returns the positive number of logical CPUs or cores based on `n_jobs`"""
    # Check if we are running under pytest
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2

    n_cpus = os.cpu_count()  # available CPUs

    # invalid n_jobs
    if abs(n_jobs) > n_cpus or n_jobs == 0:
        cpu_count = n_cpus

    # getting positive n_jobs
    if n_jobs < 0:
        cpu_count = n_cpus + 1 + n_jobs
    else:
        cpu_count = n_jobs

    return cpu_count
