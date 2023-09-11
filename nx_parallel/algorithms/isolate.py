from joblib import Parallel, cpu_count, delayed
import networkx as nx
from nx_parallel.algorithms.utils.chunk import chunks

__all__ = ["number_of_isolates"]


def number_of_isolates(G):
    """Returns the number of isolates in the graph. Parallel implementation.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    """
    isolates_list = list(nx.isolates.__wrapped__(G.graph_object))
    num_chunks = max(len(isolates_list) // cpu_count(), 1)
    isolate_chunks = chunks(isolates_list, num_chunks)
    results = Parallel(n_jobs=-1)(delayed(len)(chunk) for chunk in isolate_chunks)
    return sum(results)
