from networkx.algorithms.shortest_paths.generic import single_source_all_shortest_paths
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "all_pairs_all_shortest_paths",
]


@nxp._configure_if_nx_active()
def all_pairs_all_shortest_paths(
    G, weight=None, method="dijkstra", get_chunks="chunks"
):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily compute all shortest paths between all nodes for
    each node in `node_chunk`, and then employs joblib's `Parallel` function to
    execute these computations in parallel across `n_jobs` number of CPU cores.

    networkx.single_source_all_shortest_paths : https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.single_source_all_shortest_paths.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` into `n_jobs` number of chunks.
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
