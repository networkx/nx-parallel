import itertools
import os
import networkx as nx


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
    """Get the positive value of `n_jobs`

    Returns the positive value of `n_jobs` by either extracting it from the
    active configuration system or modifying the passed-in value, similar to
    joblib's behavior.

    - If running under pytest, it returns 2 jobs.
    - If the `active` configuration in NetworkX's config is `True`, `n_jobs`
      is extracted from the NetworkX config.
    - Otherwise, `n_jobs` is obtained from joblib's active backend.
    - `ValueError` is raised if `n_jobs` is 0.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2

    if n_jobs is None:
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


def create_iterables(G, iterator, n_cores, list_of_iterator=None):
    """Create an iterable of function inputs for parallel computation
    based on the provided iterator type.

    Parameters
    ----------
    G : NetworkX graph
        The NetworkX graph.
    iterator : str
        Type of iterator. Valid values are 'node', 'edge', 'isolate'
    n_cores : int
        The number of cores to use.
    list_of_iterator : list, optional
        A precomputed list of items to iterate over. If None, it will
        be generated based on the iterator type.

    Returns
    -------
    iterable : Iterable
        An iterable of function inputs.

    Raises
    ------
    ValueError
        If the iterator type is not one of "node", "edge" or "isolate".
    """

    if not list_of_iterator:
        if iterator == "node":
            list_of_iterator = list(G.nodes)
        elif iterator == "edge":
            list_of_iterator = list(G.edges)
        elif iterator == "isolate":
            list_of_iterator = list(nx.isolates(G))
        else:
            raise ValueError(f"Invalid iterator type: {iterator}")

    if not list_of_iterator:
        return iter([])

    return chunks(list_of_iterator, n_cores)
