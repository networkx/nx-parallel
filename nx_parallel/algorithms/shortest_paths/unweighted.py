# TODO : update docstrings

"""
Shortest path parallel algorithms for unweighted graphs.
"""

from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.shortest_paths.unweighted import (
    single_source_shortest_path_length,
    single_source_shortest_path,
)

__all__ = [
    "all_pairs_shortest_path",
    "all_pairs_shortest_path_length",
]


def all_pairs_shortest_path_length(G, cutoff=None):
    """Computes the shortest path lengths between all nodes in `G`."""
    if hasattr(G, "graph_object"):
        G = G.graph_object

    length = single_source_shortest_path_length

    def _calculate_all_pairs_shortest_path_length_subset(n):
        return (n, (length(G, n, cutoff=cutoff)))

    total_cores = nxp.cpu_count()

    return Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_all_pairs_shortest_path_length_subset)(n) for n in G
    )


def all_pairs_shortest_path(G, cutoff=None):
    """Compute shortest paths between all nodes."""
    if hasattr(G, "graph_object"):
        G = G.graph_object

    def _calculate_all_pairs_shortest_path_subset(n):
        return (n, (single_source_shortest_path(G, n, cutoff=cutoff)))

    total_cores = nxp.cpu_count()

    return Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_all_pairs_shortest_path_subset)(n) for n in G
    )
