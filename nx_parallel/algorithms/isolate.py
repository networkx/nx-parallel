import networkx as nx
from joblib import Parallel, delayed

import nx_parallel as nxp

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
    if hasattr(G, "graph_object"):
        G = G.graph_object
    isolates_list = list(nx.isolates(G))
    num_in_chunk = max(len(isolates_list) // nxp.cpu_count(), 1)
    isolate_chunks = nxp.chunks(isolates_list, num_in_chunk)
    results = Parallel(n_jobs=-1)(delayed(len)(chunk) for chunk in isolate_chunks)
    return sum(results)
