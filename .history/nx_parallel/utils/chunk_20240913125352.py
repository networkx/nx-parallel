import itertools
import os
import networkx as nx

from nx_parallel.utils.types import GraphIteratorType


__all__ = ["chunks", "get_n_jobs", "create_iterables"]


def chunks(iterable, n_chunks):
    """Yield exactly `n_chunks` chunks from `iterable`, balancing the chunk sizes."""
    iterable = list(iterable)
    k, m = divmod(len(iterable), n_chunks)
    it = iter(iterable)
    for _ in range(n_chunks):
        chunk_size = k + (1 if m > 0 else 0)
        m -= 1
        yield tuple(itertools.islice(it, chunk_size))


def get_n_jobs(n_jobs=None):
    """
    Return the positive value of `n_jobs`, adjusting for the environment.

    If running under pytest, returns 2 jobs. If using a parallel backend,
    returns the number of jobs configured for the backend. Otherwise, returns
    the number of CPUs adjusted for negative `n_jobs` values.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2

    if n_jobs == 0:
        raise ValueError("n_jobs == 0 in Parallel has no meaning")

    if not n_jobs:
        if nx.config.backends.parallel.active:
            n_jobs = nx.config.backends.parallel.n_jobs
        else:
            from joblib.parallel import get_active_backend

            n_jobs = get_active_backend()[1]

    if not n_jobs:
        return 1  # Default to 1 if no valid n_jobs is found or passed
    if n_jobs < 0:
        return os.cpu_count() + n_jobs + 1

    return int(n_jobs)


def create_iterables(
    G,
    iterator,
    n_cores,
    list_of_iterator=None,
):
    """
    Create an iterable of function inputs for parallel computation
    based on the provided iterator type.

    Parameters
    ----------
    G : networkx.Graph
        The NetworkX graph.
    iterator : GraphIteratorType
        Type of iterator. Valid values are 'NODE', 'EDGE', 'ISOLATE'.
    n_cores : int
        The number of cores to use.
    list_of_iterator : list, optional
        A precomputed list of items to iterate over. If None, it will
        be generated based on the iterator type.

    Returns
    -------
    iterable
        An iterable of function inputs.

    Raises
    ------
    ValueError
        If the iterator type is not valid.
    """
    if not list_of_iterator:
        if iterator == GraphIteratorType.NODE:
            list_of_iterator = list(G.nodes)
        elif iterator == GraphIteratorType.EDGE:
            list_of_iterator = list(G.edges)
        elif iterator == GraphIteratorType.ISOLATE:
            list_of_iterator = list(nx.isolates(G))
        else:
            raise ValueError(f"Invalid iterator type: {iterator}")

    if not list_of_iterator:
        return iter([])

    return chunks(list_of_iterator, n_cores)
