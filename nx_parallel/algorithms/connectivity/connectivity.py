"""
Parallel flow based connectivity algorithms
"""

import itertools
from networkx.algorithms.flow import build_residual_network
from networkx.algorithms.connectivity.utils import build_auxiliary_node_connectivity
from networkx.algorithms.connectivity.connectivity import local_node_connectivity
from joblib import Parallel, delayed

__all__ = [
    "all_pairs_node_connectivity",
]


def all_pairs_node_connectivity(G, nbunch=None, flow_func=None):
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

    # Reuse auxiliary digraph and residual network
    H = build_auxiliary_node_connectivity(G)
    R = build_residual_network(H, "capacity")
    kwargs = {"flow_func": flow_func, "auxiliary": H, "residual": R}

    def _compute_local_node_connectivity(u, v):
        K = local_node_connectivity(G, u, v, **kwargs)
        return u, v, K

    results = Parallel(n_jobs=-1)(
        delayed(_compute_local_node_connectivity)(u, v) for u, v in iter_func(nbunch, 2)
    )

    for u, v, K in results:
        all_pairs[u][v] = K
        if not directed:
            all_pairs[v][u] = K

    return all_pairs
