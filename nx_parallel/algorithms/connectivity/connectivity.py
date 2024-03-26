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
    """The parallel implementation first divides a list of all permutation (in case
    of directed graphs) and combinations (in case of undirected graphs) of `nbunch`
    into chunks and then creates a generator to lazily compute the local node
    connectivities for each chunk, and then employs joblib's `Parallel` function to
    execute these computations in parallel across all available CPU cores. At the end,
    the results are aggregated into a single dictionary and returned.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in `list(iter_func(nbunch, 2))` as input and returns
        an iterable `pairs_chunks`, here `iter_func` is `permutations` in case of
        directed graphs and `combinations` in case of undirected graphs. The default
        is to create chunks by slicing the list into `n` chunks, where `n` is the
        number of CPU cores, such that size of each chunk is atmost 10, and at least 1.

    networkx.all_pairs_node_connectivity : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.connectivity.all_pairs_node_connectivity.html
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
        num_in_chunk = max(min(len(pairs) // total_cores, 10), 1)
        pairs_chunks = nxp.chunks(pairs, num_in_chunk)
    else:
        pairs_chunks = get_chunks(pairs)

    nc_chunk_generator = (  # nc = node connectivity
        delayed(_process_pair_chunk)(pairs_chunk) for pairs_chunk in pairs_chunks
    )

    for nc_chunk in Parallel(n_jobs=total_cores)(nc_chunk_generator):
        for u, v, k in nc_chunk:
            all_pairs[u][v] = k
            if not directed:
                all_pairs[v][u] = k
    return all_pairs
