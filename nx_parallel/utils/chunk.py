import itertools
import os
import threading
from contextlib import contextmanager
import networkx as nx
import nx_parallel as nxp
from joblib import Parallel, delayed

__all__ = ["parallel_config", "chunks", "get_n_jobs", "execute_parallel"]

_joblib_config = (
    threading.local()
)  # thread-local storage ensures that parallel configs are thread-safe and do not
# interfere with each other during concurrent executions.


@contextmanager
def parallel_config(**kwargs):
    """Context manager to temporarily override Joblib's Parallel configurations.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments corresponding to Joblib's Parallel parameters
        (e.g., backend, verbose). These overrides are temporary and confined
        to the current thread.
    """
    original_kwargs = getattr(_joblib_config, "parallel_kwargs", {}).copy()
    _joblib_config.parallel_kwargs = {**original_kwargs, **kwargs}

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

    - If running under pytest, it returns 2 jobs when n_jobs is None.
    - If the `active` configuration in NetworkX's config is `True`, `n_jobs`
      is extracted from the NetworkX config.
    - Otherwise, `n_jobs` is obtained from joblib's active backend.
    - `ValueError` is raised if `n_jobs` is 0.
    """
    parallel_kwargs = getattr(_joblib_config, "parallel_kwargs", {})
    if n_jobs is None and "n_jobs" in parallel_kwargs:
        n_jobs = parallel_kwargs["n_jobs"]

    if n_jobs is None and "PYTEST_CURRENT_TEST" in os.environ:
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
    G,
    process_func,
    iterator_func,
    get_chunks="chunks",
    **kwargs,
):
    """Helper function to execute a processing function in parallel over chunks of data.

    Parameters
    ----------
    G : networkx.Graph or ParallelGraph
        The graph on which the algorithm operates.
    process_func : callable
        The function to process each chunk. Should accept (G, chunk, **kwargs).
    iterator_func : callable
        A function that takes G and returns an iterable of data to process.
    get_chunks : str or callable, optional (default="chunks")
        Determines how to chunk the data.
            - If "chunks" or "nodes", chunks are created automatically based on the
            number of jobs.
            - If callable, it should take the data iterable and return an iterable of
            chunks.
    **kwargs : dict
        Additional keyword arguments to pass to `process_func`.

    Returns
    -------
    list
        A list of results from each parallel execution.
    """
    n_jobs = nxp.get_n_jobs()

    if hasattr(G, "graph_object"):
        G = G.graph_object

    data = iterator_func(G)

    if get_chunks in {"chunks", "nodes"}:
        data = list(data)
        data_chunks = nxp.chunks(data, max(len(data) // n_jobs, 1))
    elif callable(get_chunks):
        data_chunks = get_chunks(data)
    else:
        raise ValueError(
            "get_chunks must be 'chunks', 'nodes', or a callable that returns an "
            "iterable of chunks."
        )

    # retrieve global backend ParallelConfig instance
    config = nx.config.backends.parallel

    joblib_params = {
        "backend": config.backend,
        "n_jobs": n_jobs,
        "verbose": config.verbose,
        "temp_folder": config.temp_folder,
        "max_nbytes": config.max_nbytes,
        "mmap_mode": config.mmap_mode,
        "prefer": config.prefer,
        "require": config.require,
        "inner_max_num_threads": config.inner_max_num_threads,
    }

    # retrieve and apply overrides from parallel_config
    parallel_kwargs = getattr(_joblib_config, "parallel_kwargs", {})
    joblib_params.update(parallel_kwargs)

    joblib_params = {k: v for k, v in joblib_params.items() if v is not None}

    return Parallel(**joblib_params)(
        delayed(process_func)(G, chunk, **kwargs) for chunk in data_chunks
    )
