from itertools import combinations
from joblib import Parallel, delayed
import nx_parallel as nxp


__all__ = [
    "v_structures",
    "colliders",
]


@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
def v_structures(G, get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily yield 3-node tuples that represent v_structures
    for each `node_chunk`, and then employs joblib's `Parallel` function to
    execute these computations in parallel across `n_jobs` number of CPU cores.

    networkx.dag.v_structures: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.v_structures.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and
        returns an iterable `node_chunks`. The default chunking is done
        by slicing the nodes into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    for p1, c, p2 in colliders(G, get_chunks=get_chunks):
        if not (G.has_edge(p1, p2) or G.has_edge(p2, p1)):
            yield (p1, c, p2)


@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
def colliders(G, get_chunks="chunks"):
    """The parallel implementation first divides the nodes into chunks and then
    creates a generator to lazily yield 3-node tuples that represent colliders
    for each `node_chunk`, and then employs joblib's `Parallel` function to execute
    these computations in parallel across `n_jobs` number of CPU cores.

    networkx.dag.colliders: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.colliders.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and
        returns an iterable `node_chunks`. The default chunking is done
        by slicing the nodes into `n_jobs` number of chunks.
    """

    def _process_chunk(chunk):
        return [
            (p1, node, p2)
            for node in chunk
            for p1, p2 in combinations(G.predecessors(node), 2)
        ]

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = list(G)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)

    collider_chunks = (delayed(_process_chunk)(chunk) for chunk in node_chunks)

    for chunk in Parallel()(collider_chunks):
        for collider in chunk:
            yield collider
