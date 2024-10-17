import itertools
import os
import threading
from contextlib import contextmanager
import networkx as nx
import nx_parallel as nxp
from joblib import Parallel, delayed

__all__ = ["chunks", "get_n_jobs", "execute_parallel"]

_joblib_config = (
    threading.local()
)  # thread-local storage ensures that parallel configs are thread-safe and do not interfere with each other during concurrent executions.


@contextmanager
def parallel_config(**kwargs):
    """
    Context manager to set Joblib's Parallel configurations in thread-local storage.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments corresponding to Joblib's Parallel parameters (e.g., backend, verbose).
    """
    original_kwargs = getattr(_joblib_config, "parallel_kwargs", {})
    _joblib_config.parallel_kwargs = kwargs
    try:
        yield
    finally:
        _joblib_config.parallel_kwargs = original_kwargs


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


def execute_parallel(
    G: nx.Graph,
    process_func,
    iterator_func,
    get_chunks="chunks",
    **kwargs,
):
    """
    Helper function to execute a processing function in parallel over chunks of data.

    Parameters
    ----------
    G : networkx.Graph
        The graph on which the algorithm operates.
    process_func : callable
        The function to process each chunk. Should accept (G, chunk, **kwargs).
    iterator_func : callable, optional
        A function that takes G and returns an iterable of data to process.
    get_chunks : str or callable, optional (default="chunks")
        Determines how to chunk the data.
            - If "chunks", chunks are created automatically based on the number of jobs.
            - If callable, it should take the data iterable and return an iterable of chunks.
    **kwargs : dict
        Additional keyword arguments to pass to `process_func`.

    Returns
    -------
    list
        A list of results from each parallel execution.
    """
    n_jobs = nxp.get_n_jobs()

    # generate data using the iterator function
    data = iterator_func(G)

    # handle chunking
    if get_chunks == "chunks":
        # convert data to a list if it's a generator or other iterable
        data = list(data)
        data_chunks = nxp.chunks(data, max(len(data) // n_jobs, 1))
    elif callable(get_chunks):
        data_chunks = get_chunks(data)
    else:
        raise ValueError(
            "get_chunks must be 'chunks' or a callable that returns an iterable of chunks."
        )

    # read parallel_kwargs from thread-local storage
    parallel_kwargs = getattr(_joblib_config, "parallel_kwargs", {})

    return Parallel()(
        delayed(process_func)(G, chunk, **kwargs) for chunk in data_chunks
    )
