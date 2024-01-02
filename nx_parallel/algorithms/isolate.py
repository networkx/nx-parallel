import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["number_of_isolates"]


def number_of_isolates(G, n_jobs=-1):
    """Parallelly computes the number of isolates in the graph.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    n_jobs : int, optional (default=-1)
        The number of logical CPUs or cores you want to use. 
        For `n_jobs` less than 0, (`n_cpus + 1 + n_jobs`) are used.
        If an invalid value is given, then `n_jobs` is set to `n_cpus`.

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    isolates_list = list(nx.isolates(G))
    num_in_chunk = max(len(isolates_list) // cpu_count, 1)
    isolate_chunks = nxp.chunks(isolates_list, num_in_chunk)
    results = Parallel(n_jobs=cpu_count)(
        delayed(len)(chunk) for chunk in isolate_chunks
    )
    return sum(results)
