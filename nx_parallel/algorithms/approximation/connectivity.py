"""Parallel implementations of fast approximation for node connectivity"""
import itertools
from joblib import Parallel, delayed
from networkx.algorithms.approximation.connectivity import local_node_connectivity

__all__ = [
    "all_pairs_node_connectivity",
]


def all_pairs_node_connectivity(G, nbunch=None, cutoff=None):
    """The parallel computation is implemented by computing the
    `local_node_connectivity` for all nodes in `G`, concurrently
    on different cores.

    networkx.all_pairs_node_connectivity : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.connectivity.all_pairs_node_connectivity.html
    """

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

    all_pairs = {n: {} for n in nbunch}

    def _compute_local_node_connectivity(u, v):
        k = local_node_connectivity(G, u, v, cutoff=cutoff)
        return u, v, k

    results = Parallel(n_jobs=-1)(
        delayed(_compute_local_node_connectivity)(u, v) for u, v in iter_func(nbunch, 2)
    )

    for u, v, k in results:
        all_pairs[u][v] = k
        if not directed:
            all_pairs[v][u] = k

    return all_pairs
