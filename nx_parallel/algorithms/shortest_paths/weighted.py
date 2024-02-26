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


def all_pairs_dijkstra(G, cutoff=None, weight="weight", get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths and lengths for each
    `node_chunk`, and then employs joblib's `Parallel` function to execute these
    computations in parallel across all available CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.all_pairs_dijkstra : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_dijkstra.html#all-pairs-dijkstra
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, (single_source_dijkstra(G, node, cutoff=cutoff, weight=weight)))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)

    paths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_chunk in Parallel(n_jobs=nxp.cpu_count())(paths_chunk_generator):
        for path in path_chunk:
            yield path


def all_pairs_dijkstra_path_length(
    G, cutoff=None, weight="weight", get_chunks="chunks"
):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths lengths for each node in
    `node_chunk`, and then employs joblib's `Parallel` function to execute these
    computations in parallel across all available CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.all_pairs_dijkstra_path_length : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_dijkstra_path_length.html#all-pairs-dijkstra-path-length
    """

    def _process_node_chunk(node_chunk):
        return [
            (
                node,
                single_source_dijkstra_path_length(
                    G, node, cutoff=cutoff, weight=weight
                ),
            )
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)

    paths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_chunk in Parallel(n_jobs=nxp.cpu_count())(paths_chunk_generator):
        for path in path_chunk:
            yield path


def all_pairs_dijkstra_path(G, cutoff=None, weight="weight", get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths for each `node_chunk`, and
    then employs joblib's `Parallel` function to execute these computations in
    parallel across all available CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.all_pairs_dijkstra_path : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_dijkstra_path.html#all-pairs-dijkstra-path
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, single_source_dijkstra_path(G, node, cutoff=cutoff, weight=weight))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)

    paths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_chunk in Parallel(n_jobs=nxp.cpu_count())(paths_chunk_generator):
        for path in path_chunk:
            yield path


def all_pairs_bellman_ford_path_length(G, weight="weight", get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths lengths for each node in
    `node_chunk`, and then employs joblib's `Parallel` function to execute these
    computations in parallel across all available CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.all_pairs_bellman_ford_path_length : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_bellman_ford_path_length.html#all-pairs-bellman-ford-path-length
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, single_source_bellman_ford_path_length(G, node, weight=weight))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)

    path_lengths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_length_chunk in Parallel(n_jobs=nxp.cpu_count())(
        path_lengths_chunk_generator
    ):
        for path_length in path_length_chunk:
            yield path_length


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
