"""
Parallel flow based connectivity algorithms
"""

import itertools
from networkx.algorithms.flow import build_residual_network
from networkx.algorithms.connectivity.utils import build_auxiliary_node_connectivity
from networkx.algorithms.connectivity.connectivity import local_node_connectivity
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "all_pairs_node_connectivity",
]


def all_pairs_node_connectivity(G, nbunch=None, flow_func=None, get_chunks="chunks"):
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

    def _process_pair_chunk(pairs_chunk):
        return [
            (u, v, local_node_connectivity(G, u, v, **kwargs)) for u, v in pairs_chunk
        ]

    pairs = list(iter_func(nbunch, 2))
    total_cores = nxp.cpu_count()
    if get_chunks == "chunks":
        num_in_chunk = min(len(pairs) // total_cores, 10)
        pairs_chunks = nxp.chunks(pairs, num_in_chunk)
    else:
        pairs_chunks = get_chunks(pairs)

    paths_chunk_generator = (
        delayed(_process_pair_chunk)(pairs_chunk) for pairs_chunk in pairs_chunks
    )

    for path_chunk in Parallel(n_jobs=total_cores)(paths_chunk_generator):
        for path in path_chunk:
            u, v, k = path
            all_pairs[u][v] = k
            if not directed:
                all_pairs[v][u] = k
    return all_pairs
