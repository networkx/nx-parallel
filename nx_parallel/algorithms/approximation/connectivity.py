"""Parallel implementations of fast approximation for node connectivity"""
import itertools
from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.approximation.connectivity import local_node_connectivity

__all__ = [
    "all_pairs_node_connectivity",
]


def all_pairs_node_connectivity(G, nbunch=None, cutoff=None):
    """The parallel computation is implemented by computing the
    `local_node_connectivity` for all nodes in `G` in chunks, concurrently 
    on different threads. Backend used is `threading`.

    networkx.all_pairs_node_connectivity : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.connectivity.all_pairs_node_connectivity.html
    """

    def _calculate_all_pairs_node_connectivity_subset(chunk, directed=False):
        for u, v in chunk:
            k = local_node_connectivity(G, u, v, cutoff=cutoff)
            all_pairs[u][v] = k
            if not directed:
                all_pairs[v][u] = k

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if nbunch is None:
        nbunch = G
    else:
        nbunch = set(nbunch)

    directed = G.is_directed()
    if directed:
        iter_func = itertools.permutations
    else:
        iter_func = itertools.combinations

    pairs = list(iter_func(nbunch, 2))

    all_pairs = {u: {v: None for v in nbunch if v != u} for u in nbunch}

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(pairs) // total_cores, 1)
    pair_chunks = nxp.chunks(pairs, num_in_chunk)

    Parallel(n_jobs=total_cores, backend="threading")(
        delayed(_calculate_all_pairs_node_connectivity_subset)(chunk, directed=directed)
        for chunk in pair_chunks
    )

    return all_pairs
