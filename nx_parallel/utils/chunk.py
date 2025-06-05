import itertools
import os
import networkx as nx


__all__ = ["chunks", "get_n_jobs", "create_iterables"]


def chunks(iterable, n_chunks, *, max_chunk_size=None):
    """Yield chunks from input iterable.

    - If `max_chunk_size` is None (default), the iterable is split into
    exactly `n_chunks` equally sized chunks.
    - If `max_chunk_size` is specified and the default split would create
    chunks larger than this size, the iterable is instead divided into
    smaller chunks, each containing at most `max_chunk_size` items.

    Parameters
    ----------
    iterable : Iterable
        An iterable of inputs to be divided.
    n_chunks : int
        The number of chunks the iterable is divided into. Ignored
        if chunks' size exceed the `max_chunk_size` value.
    max_chunk_size : int, optional (default = None)
        Maximum number of items allowed in each chunk. If None, it
        divides the iterable into `n_chunks` chunks.

    Examples
    --------
    >>> import nx_parallel as nxp
    >>> data = list(range(10))
    >>> list(nxp.chunks(data, 3))
    [(0, 1, 2, 3), (4, 5, 6), (7, 8, 9)]
    >>> list(nxp.chunks(data, 3, max_chunk_size=2))
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    >>> list(nxp.chunks(data, 5, max_chunk_size=3))
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    """
    iterable = list(iterable)
    base_chunk_size, extra_items = divmod(len(iterable), n_chunks)
    if max_chunk_size and base_chunk_size >= max_chunk_size:
        yield from itertools.batched(iterable, max_chunk_size)
        return

    it = iter(iterable)
    for _ in range(n_chunks):
        chunk_size = base_chunk_size + (1 if extra_items > 0 else 0)
        extra_items -= 1
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


def create_iterables(G, iterator, n_jobs, list_of_iterator=None):
    """Create an iterable of function inputs for parallel computation
    based on the provided iterator type.

    Parameters
    ----------
    G : NetworkX graph
        The NetworkX graph.
    iterator : str
        Type of iterator. Valid values are 'node', 'edge', 'isolate'
    n_jobs : int
        The number of parallel jobs to run.
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

    return chunks(list_of_iterator, n_jobs)
