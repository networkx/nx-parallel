import itertools
import os
import networkx as nx
from dataclasses import asdict

__all__ = [
    "chunks",
    "cpu_count",
    "create_iterables",
    "get_config",
]


def chunks(iterable, n):
    """Divides an iterable into chunks of size n"""
    it = iter(iterable)
    while True:
        x = tuple(itertools.islice(it, n))
        if not x:
            return
        yield x


def cpu_count(n_jobs=None):  # todo: rename to get_n_jobs
    """Returns the positive value of `n_jobs`."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2
    else:
        n_cpus = os.cpu_count()
        if n_jobs is None:
            return 1
        if n_jobs < 0:
            return n_cpus + n_jobs + 1
        if n_jobs == 0:
            raise ValueError("n_jobs == 0 in Parallel has no meaning")
        return int(n_jobs)


def create_iterables(G, iterator, n_cores, list_of_iterator=None):
    """Creates an iterable of function inputs for parallel computation
    based on the provided iterator type.

    Parameters
    -----------
    G : NetworkX graph
    iterator : str
        Type of iterator. Valid values are 'node', 'edge', 'isolate'

    Returns:
    --------
    iterable : Iterable
        An iterable of function inputs.
    """

    if iterator in ["node", "edge", "isolate"]:
        if list_of_iterator is None:
            if iterator == "node":
                list_of_iterator = list(G.nodes)
            elif iterator == "edge":
                list_of_iterator = list(G.edges)
            elif iterator == "isolate":
                list_of_iterator = list(nx.isolates(G))
        num_in_chunk = max(len(list_of_iterator) // n_cores, 1)
        return chunks(list_of_iterator, num_in_chunk)
    else:
        raise ValueError("Invalid iterator type.")


def _get_config(config):
    config_dict = asdict(config)
    config_dict.update(config_dict["backend_params"])
    del config_dict["backend_params"]
    config_dict["n_jobs"] = cpu_count(config_dict["n_jobs"])
    return config_dict


def get_config(config=None):
    """Returns the current configuration settings for nx_parallel."""
    config_dict = _get_config(nx.config.backends.parallel)
    if config is None:
        return config_dict
    elif config in config_dict:
        return config_dict[config]
    else:
        raise KeyError(f"Invalid config: {config}")
