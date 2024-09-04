import itertools
import os
import networkx as nx
from typing import Iterable, Iterator, Optional, List, Union

from nx_parallel.utils import NX_GTYPES


__all__ = ["chunks", "get_n_jobs", "create_iterables"]


def chunks(iterable: Iterable, n: int) -> Iterator[tuple]:
    """Yield successive chunks of size n from an iterable."""
    it = iter(iterable)
    yield from iter(lambda: tuple(itertools.islice(it, n)), ())


def get_n_jobs(n_jobs: Optional[int] = None) -> int:
    """
    Return the positive value of `n_jobs`, adjusting for the environment.

    If running under pytest, returns 2 jobs. If using a parallel backend,
    returns the number of jobs configured for the backend. Otherwise, returns
    the number of CPUs adjusted for negative `n_jobs` values.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2

    if nx.config.backends.parallel.active:
        n_jobs = nx.config.backends.parallel.n_jobs
    else:
        from joblib.parallel import get_active_backend

        n_jobs = get_active_backend()[1]

    if n_jobs is None:
        return 1
    if n_jobs < 0:
        return os.cpu_count() + n_jobs + 1
    if n_jobs == 0:
        raise ValueError("n_jobs == 0 in Parallel has no meaning")
    return int(n_jobs)


def create_iterables(
    G: NX_GTYPES,
    iterator: str,
    n_cores: int,
    list_of_iterator: Optional[Union[List, Iterable]] = None,
) -> Iterator[Union[List, Iterable]]:
    """
    Create an iterable of function inputs for parallel computation
    based on the provided iterator type.

    Parameters
    ----------
    G : networkx.Graph
        The NetworkX graph.
    iterator : str
        Type of iterator. Valid values are 'node', 'edge', 'isolate'.
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
    if list_of_iterator is None:
        if iterator == "node":
            iter_func = G.nodes
        elif iterator == "edge":
            iter_func = G.edges
        elif iterator == "isolate":
            iter_func = lambda: nx.isolates(G)
        else:
            raise ValueError(f"Invalid iterator type: {iterator}")

        # Instead of creating a list, use the generator directly in chunks
        list_of_iterator = iter_func()

    num_in_chunk = (
        max(len(list(G)) // n_cores, 1)
        if isinstance(list_of_iterator, list)
        else n_cores
    )
    return chunks(list_of_iterator, num_in_chunk)
