from networkx.algorithms.shortest_paths.generic import single_source_all_shortest_paths
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "all_pairs_all_shortest_paths",
]


def all_pairs_all_shortest_paths(
    G, weight=None, method="dijkstra", get_chunks="chunks"
):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute all shortest paths between all nodes for
    each node in `node_chunk`, and then employs joblib's `Parallel` function to
    execute these computations in parallel across all available CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.single_source_all_shortest_paths : https://github.com/networkx/networkx/blob/de85e3fe52879f819e7a7924474fc6be3994e8e4/networkx/algorithms/shortest_paths/generic.py#L606
    """

    def _process_node_chunk(node_chunk):
        return [
            (
                n,
                dict(
                    single_source_all_shortest_paths(G, n, weight=weight, method=method)
                ),
            )
            for n in node_chunk
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

    for path_chunk in Parallel(n_jobs=total_cores)(paths_chunk_generator):
        for path in path_chunk:
            yield path
