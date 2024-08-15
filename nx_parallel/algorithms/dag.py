from itertools import combinations
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "v_structures",
    "colliders",
]


def v_structures(G, get_chunks="chunks"):
    """Yields 3-node tuples that represent the v-structures in `G` in parallel.

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and
        returns an iterable `node_chunks`. The default chunking is done
        by slicing the nodes into `n_jobs` number of chunks.
    """
    colliders = nxp.dag.colliders(G, get_chunks=get_chunks)
    if hasattr(G, "graph_object"):
        G = G.graph_object
    for p1, c, p2 in colliders:
        if not (G.has_edge(p1, p2) or G.has_edge(p2, p1)):
            yield (p1, c, p2)


def colliders(G, get_chunks="chunks"):
    """Yields 3-node tuples that represent the colliders in `G` in parallel.

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and
        returns an iterable `node_chunks`. The default chunking is done
        by slicing the nodes into `n_jobs` number of chunks.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = list(G.nodes)
    n_jobs = nxp.cpu_count()
    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // n_jobs, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)

    def _process_chunk(chunk):
        return [
            (p1, node, p2)
            for node in chunk
            for p1, p2 in combinations(G.predecessors(node), 2)
        ]

    collider_chunk_generator = (delayed(_process_chunk)(chunk) for chunk in node_chunks)

    for collider_chunk in Parallel(n_jobs=n_jobs)(collider_chunk_generator):
        for collider in collider_chunk:
            yield collider
