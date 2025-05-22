"""Parallel implementations of fast approximation for node connectivity"""

import itertools
from joblib import Parallel, delayed
from networkx.algorithms.approximation.connectivity import local_node_connectivity
import nx_parallel as nxp

__all__ = [
    "approximate_all_pairs_node_connectivity",
]


@nxp._configure_if_nx_active()
def approximate_all_pairs_node_connectivity(
    G, nbunch=None, cutoff=None, get_chunks="chunks"
):
    """The parallel implementation first divides the a list of all permutation (in case
    of directed graphs) and combinations (in case of undirected graphs) of `nbunch`
    into chunks and then creates a generator to lazily compute the local node
    connectivities for each chunk, and then employs joblib's `Parallel` function to
    execute these computations in parallel across `n_jobs` number of CPU cores. At the
    end, the results are aggregated into a single dictionary and returned.

    Note, this function uses the name `approximate_all_pairs_node_connectivity` while
    dispatching to the backend in=mplementation. So, `nxp.all_pairs_node_connectivity`
    will run the parallel implementation of `all_pairs_node_connectivity` present in the
    `connectivity/connectivity`. Use `nxp.approximate_all_pairs_node_connectivity` instead.

    networkx.all_pairs_node_connectivity : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.connectivity.all_pairs_node_connectivity.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in `list(iter_func(nbunch, 2))` as input and returns
        an iterable `pairs_chunks`, here `iter_func` is `permutations` in case of
        directed graphs and `combinations` in case of undirected graphs. The default
        is to create chunks by slicing the list into `n_jobs` chunks, such that size
        of each chunk is atmost 10, and at least 1.
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

    def _process_pair_chunk(pairs_chunk):
        return [
            (u, v, local_node_connectivity(G, u, v, cutoff=cutoff))
            for u, v in pairs_chunk
        ]

    pairs = list(iter_func(nbunch, 2))
    n_jobs = nxp.get_n_jobs()
    if get_chunks == "chunks":
        pairs_chunks = nxp.chunks(pairs, n_jobs, max_chunk_size=10)
    else:
        pairs_chunks = get_chunks(pairs)

    nc_chunk_generator = (  # nc = node connectivity
        delayed(_process_pair_chunk)(pairs_chunk) for pairs_chunk in pairs_chunks
    )

    for nc_chunk in Parallel()(nc_chunk_generator):
        for u, v, k in nc_chunk:
            all_pairs[u][v] = k
            if not directed:
                all_pairs[v][u] = k
    return all_pairs
