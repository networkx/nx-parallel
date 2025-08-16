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


@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
def all_pairs_shortest_path_length(G, cutoff=None, get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths lengths for each node in
    `node_chunk`, and then employs joblib's `Parallel` function to execute these
    computations in parallel across `n_jobs` number of CPU cores.

    networkx.single_source_shortest_path_length : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path_length.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n_jobs` number of chunks.
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, single_source_shortest_path_length(G, node, cutoff=cutoff))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)

    path_lengths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_length_chunk in Parallel()(path_lengths_chunk_generator):
        for path_length in path_length_chunk:
            yield path_length


@nxp._configure_if_nx_active()
def all_pairs_shortest_path(G, cutoff=None, get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths for each `node_chunk`, and
    then employs joblib's `Parallel` function to execute these computations in
    parallel across `n_jobs` number of CPU cores.

    networkx.single_source_shortest_path : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n_jobs` number of chunks.
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, single_source_shortest_path(G, node, cutoff=cutoff))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)

    paths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_chunk in Parallel()(paths_chunk_generator):
        for path in path_chunk:
            yield path
