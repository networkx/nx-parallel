# TODO : update docstrings

"""
Shortest path parallel algorithms for weighted graphs.
"""

from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.shortest_paths.weighted import (
    single_source_dijkstra,
    single_source_dijkstra_path_length,
    single_source_dijkstra_path,
    single_source_bellman_ford_path,
    single_source_bellman_ford_path_length,
)

__all__ = [
    "all_pairs_dijkstra",
    "all_pairs_dijkstra_path_length",
    "all_pairs_dijkstra_path",
    "all_pairs_bellman_ford_path_length",
    "all_pairs_bellman_ford_path",
]


def all_pairs_dijkstra(G, cutoff=None, weight="weight"):
    """Find shortest weighted paths and lengths between all nodes."""

    def _calculate_all_pairs_dijkstra_subset(n):
        return (n, (single_source_dijkstra(G, n, cutoff=cutoff, weight=weight)))

    total_cores = nxp.cpu_count()

    return Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_all_pairs_dijkstra_subset)(n) for n in G
    )


def all_pairs_dijkstra_path_length(G, cutoff=None, weight="weight"):
    """Compute shortest path lengths between all nodes in a weighted graph."""
    length = single_source_dijkstra_path_length

    def _calculate_all_pairs_dijkstra_path_length_subset(n):
        return (n, (length(G, n, cutoff=cutoff, weight=weight)))

    total_cores = nxp.cpu_count()

    return Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_all_pairs_dijkstra_path_length_subset)(n) for n in G
    )


def all_pairs_dijkstra_path(G, cutoff=None, weight="weight"):
    """Compute shortest paths between all nodes in a weighted graph."""
    path = single_source_dijkstra_path

    def _calculate_all_pairs_dijkstra_path_subset(n):
        return (n, path(G, n, cutoff=cutoff, weight=weight))

    total_cores = nxp.cpu_count()

    return Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_all_pairs_dijkstra_path_subset)(n) for n in G
    )


def all_pairs_bellman_ford_path_length(G, weight="weight"):
    """Compute shortest path lengths between all nodes in a weighted graph."""

    def _calculate_shortest_paths_length_subset(n):
        return (n, dict(length(G, n, weight=weight)))

    length = single_source_bellman_ford_path_length
    total_cores = nxp.cpu_count()

    distance = Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_shortest_paths_length_subset)(n) for n in G
    )
    return distance


def all_pairs_bellman_ford_path(G, weight="weight"):
    """The parallel computation is implemented by computing the 
    shortest paths for each node concurrently.

    networkx.all_pairs_bellman_ford_path : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_bellman_ford_path.html#all-pairs-bellman-ford-path
    """

    def _calculate_shortest_paths_subset(source):
        return (source, single_source_bellman_ford_path(G, source, weight=weight))

    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    nodes = G.nodes

    paths = Parallel(n_jobs=cpu_count, return_as="generator")(
        delayed(_calculate_shortest_paths_subset)(source) for source in nodes
    )
    return paths
