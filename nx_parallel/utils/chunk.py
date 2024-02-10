import itertools
import os
import networkx as nx

__all__ = ["chunks", "cpu_count", "create_iterables"]


def chunks(iterable, n):
    """Divides an iterable into chunks of size n"""
    it = iter(iterable)
    while True:
        x = tuple(itertools.islice(it, n))
        if not x:
            return
        yield x


def cpu_count():
    """Returns the number of logical CPUs or cores"""
    # Check if we are running under pytest
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2
    return os.cpu_count()


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
