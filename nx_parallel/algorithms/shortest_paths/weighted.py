from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import (
    _weight_function,
    _dijkstra,
    _bellman_ford,
    single_source_bellman_ford_path,
)
import nx_parallel as nxp

__all__ = [
    "all_pairs_bellman_ford_path",
    "johnson",
]


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


def johnson(G, weight="weight"):
    """Uses Johnson's Algorithm to compute shortest paths."""
    if hasattr(G, "graph_object"):
        G = G.graph_object

    dist = {v: 0 for v in G}
    pred = {v: [] for v in G}
    weight = _weight_function(G, weight)

    # Calculate distance of shortest paths
    dist_bellman = _bellman_ford(G, list(G), weight, pred=pred, dist=dist)

    # Update the weight function to take into account the Bellman--Ford
    # relaxation distances.
    def new_weight(u, v, d):
        return weight(u, v, d) + dist_bellman[u] - dist_bellman[v]

    def dist_path(v):
        paths = {v: [v]}
        _dijkstra(G, v, new_weight, paths=paths)
        return paths

    def _johnson_subset(chunk):
        return {node: dist_path(node) for node in chunk}

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(G.nodes) // total_cores, 1)
    node_chunks = nxp.chunks(G.nodes, num_in_chunk)

    results = Parallel(n_jobs=total_cores)(
        delayed(_johnson_subset)(chunk) for chunk in node_chunks
    )
    return {v: d_path for result_chunk in results for v, d_path in result_chunk.items()}
