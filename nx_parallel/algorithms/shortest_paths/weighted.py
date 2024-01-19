# TODO : update docstrings

"""
Shortest path parallel algorithms for weighted graphs.
"""

from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import (
    _weight_function,
    _dijkstra_multisource,
    _dijkstra,
    _bellman_ford,
    single_source_bellman_ford_path,
    single_source_bellman_ford_path_length,
)

__all__ = [
    "dijkstra_path",
    "single_source_dijkstra_path",
    "single_source_dijkstra_path_length",
    "single_source_dijkstra",
    "multi_source_dijkstra_path",
    "multi_source_dijkstra_path_length",
    "multi_source_dijkstra",
    "all_pairs_dijkstra",
    "all_pairs_dijkstra_path_length",
    "all_pairs_dijkstra_path",
    "all_pairs_bellman_ford_path_length",
    "all_pairs_bellman_ford_path",
    "johnson",
]


def dijkstra_path(G, source, target, weight="weight"):
    """Returns the shortest weighted path from source to target in G.

    Uses Dijkstra's Method to compute the shortest weighted path
    between two nodes in a graph."""
    (length, path) = single_source_dijkstra(G, source, target=target, weight=weight)
    return path


def single_source_dijkstra_path(G, source, cutoff=None, weight="weight"):
    """Find shortest weighted paths in G from a source node.

    Compute shortest path between source and all other reachable
    nodes for a weighted graph."""
    return multi_source_dijkstra_path(G, {source}, cutoff=cutoff, weight=weight)


def single_source_dijkstra_path_length(G, source, cutoff=None, weight="weight"):
    """Find shortest weighted path lengths in G from a source node.

    Compute the shortest path length between source and all other
    reachable nodes for a weighted graph."""
    return multi_source_dijkstra_path_length(G, {source}, cutoff=cutoff, weight=weight)


def single_source_dijkstra(G, source, target=None, cutoff=None, weight="weight"):
    """Find shortest weighted paths and lengths from a source node.

    Compute the shortest path length between source and all other
    reachable nodes for a weighted graph.

    Uses Dijkstra's algorithm to compute shortest paths and lengths
    between a source and all other reachable nodes in a weighted graph."""
    return multi_source_dijkstra(
        G, {source}, cutoff=cutoff, target=target, weight=weight
    )


def multi_source_dijkstra_path(G, sources, cutoff=None, weight="weight"):
    """Find shortest weighted paths in G from a given set of source
    nodes.

    Compute shortest path between any of the source nodes and all other
    reachable nodes for a weighted graph."""
    length, path = multi_source_dijkstra(G, sources, cutoff=cutoff, weight=weight)
    return path


def multi_source_dijkstra_path_length(G, sources, cutoff=None, weight="weight"):
    """Find shortest weighted path lengths in G from a given set of
    source nodes.

    Compute the shortest path length between any of the source nodes and
    all other reachable nodes for a weighted graph."""

    def _check_node_presence_subset(nodes):
        for node in nodes:
            if node not in G:
                raise nx.NodeNotFound(f"Node {node} not found in graph")

    if not sources:
        raise ValueError("sources must not be empty")

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(sources) // total_cores, 1)
    node_chunks = nxp.chunks(sources, num_in_chunk)
    Parallel(n_jobs=total_cores)(
        delayed(_check_node_presence_subset)(chunk) for chunk in node_chunks
    )

    weight = _weight_function(G, weight)
    return _dijkstra_multisource(G, sources, weight, cutoff=cutoff)


def multi_source_dijkstra(G, sources, target=None, cutoff=None, weight="weight"):
    """Find shortest weighted paths and lengths from a given set of
    source nodes.

    Uses Dijkstra's algorithm to compute the shortest paths and lengths
    between one of the source nodes and the given `target`, or all other
    reachable nodes if not specified, for a weighted graph."""

    def _check_node_presence_subset(nodes):
        for node in nodes:
            if node not in G:
                raise nx.NodeNotFound(f"Node {node} not found in graph")

    def _initialize_paths_subset(chunk):
        paths_chunk = {source: [source] for source in chunk}
        return paths_chunk

    if not sources:
        raise ValueError("sources must not be empty")

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(sources) // total_cores, 1)
    node_chunks = nxp.chunks(sources, num_in_chunk)

    Parallel(n_jobs=total_cores)(
        delayed(_check_node_presence_subset)(chunk) for chunk in node_chunks
    )

    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)

    results = Parallel(n_jobs=total_cores)(
        delayed(_initialize_paths_subset)(chunk) for chunk in node_chunks
    )
    paths = {
        source: path
        for result_chunk in results
        for source, path in result_chunk.items()
    }

    dist = _dijkstra_multisource(
        G, sources, weight, paths=paths, cutoff=cutoff, target=target
    )
    if target is None:
        return (dist, paths)
    try:
        return (dist[target], paths[target])
    except KeyError as err:
        raise nx.NetworkXNoPath(f"No path to {target}.") from err


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


def johnson(G, weight="weight"):
    """Uses Johnson's Algorithm to compute shortest paths."""
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
