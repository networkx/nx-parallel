from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import single_source_bellman_ford_path
import nx_parallel as nxp

__all__ = [
    "all_pairs_bellman_ford_path",
]


def all_pairs_bellman_ford_path(G, weight="weight", get_chunks=None):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute shortest paths for each node_chunk, and
    then employs joblib's `Parallel` function to execute these computations in
    parallel across all available CPU cores.

    Parameters 
    ------------
    get_chunks : function (default = None)
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`

    networkx.all_pairs_bellman_ford_path : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_bellman_ford_path.html#all-pairs-bellman-ford-path
    """

    def _process_node_chunk(node_chunk):
        return [
            (node, single_source_bellman_ford_path(G, node, weight=weight))
            for node in node_chunk
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes
    total_cores = nxp.cpu_count()

    if get_chunks:
        node_chunks = get_chunks(nodes)
    else:
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)

    paths_chunk_generator = (
        delayed(_process_node_chunk)(node_chunk) for node_chunk in node_chunks
    )

    for path_chunk in Parallel(n_jobs=nxp.cpu_count())(paths_chunk_generator):
        for path in path_chunk:
            yield path
