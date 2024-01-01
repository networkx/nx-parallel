import networkx as nx
from joblib import Parallel, delayed
import os
import nx_parallel as nxp

__all__ = ["number_of_isolates"]


def number_of_isolates(G, n_jobs=-1):
    """Returns the number of isolates in the graph. Parallel implementation.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    n_jobs : int, optional (default=-1)
        The number of logical CPUs or cores you want to use. 
        If `-1` all available cores are used.
        For `n_jobs` less than `-1`, (`n_cpus + 1 + n_jobs`) are used.
        If an invalid value is given, then `n_jobs` is set to `os.cpu_count()`.

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_cpus = os.cpu_count()
    if abs(n_jobs) > n_cpus:
        n_jobs = n_cpus
    if n_jobs < 0:
        n_jobs = n_cpus + 1 + n_jobs

    isolates_list = list(nx.isolates(G))
    num_in_chunk = max(len(isolates_list) // n_jobs, 1)
    isolate_chunks = nxp.chunks(isolates_list, num_in_chunk)
    results = Parallel(n_jobs=n_jobs)(delayed(len)(chunk) for chunk in isolate_chunks)
    return sum(results)
