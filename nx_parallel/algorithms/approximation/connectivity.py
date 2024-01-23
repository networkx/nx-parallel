"""Parallel implementations of fast approximation for node connectivity"""
import itertools
from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.approximation.connectivity import local_node_connectivity

__all__ = ["all_pairs_node_connectivity",]


def all_pairs_node_connectivity(G, nbunch=None, cutoff=None):
    def _calculate_all_pairs_node_connectivity_subset(chunk):
        d = {}
        for u, v in chunk:
            k = local_node_connectivity(G, u, v, cutoff=cutoff)
            d[u][v] = k
            if not directed:
                d[v][u] = k
        return d

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

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(pairs) // total_cores, 1)
    pair_chunks = nxp.chunks(pairs, num_in_chunk)

    all_pairs = {n: {} for n in nbunch}

    results = Parallel(n_jobs=total_cores)(
        delayed(_calculate_all_pairs_node_connectivity_subset)(chunk) for chunk in pair_chunks
    )
    
    all_pairs = {u: all_pairs[u].update(values) for result in results for u, values in result.items()}
    return all_pairs
