from itertools import combinations, chain
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "square_clustering",
]


def square_clustering(G, nodes=None, get_chunks="chunks"):
    """The nodes are chunked into `node_chunks` and then the square clustering
    coefficient for all `node_chunks` are computed in parallel over all available
    CPU cores.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.square_clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.square_clustering.html
    """

    def _compute_clustering_chunk(node_iter_chunk):
        result_chunk = []
        for v in node_iter_chunk:
            clustering = 0
            potential = 0
            for u, w in combinations(G[v], 2):
                squares = len((set(G[u]) & set(G[w])) - {v})
                clustering += squares
                degm = squares + 1
                if w in G[u]:
                    degm += 1
                potential += (len(G[u]) - degm) + (len(G[w]) - degm) + squares
            if potential > 0:
                clustering /= potential
            result_chunk += [(v, clustering)]
        return result_chunk

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if nodes is None:
        node_iter = list(G)
    else:
        node_iter = list(G.nbunch_iter(nodes))

    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        num_in_chunk = max(len(node_iter) // total_cores, 1)
        node_iter_chunks = nxp.chunks(node_iter, num_in_chunk)
    else:
        node_iter_chunks = get_chunks(node_iter)

    result = Parallel(n_jobs=total_cores)(
        delayed(_compute_clustering_chunk)(node_iter_chunk)
        for node_iter_chunk in node_iter_chunks
    )
    clustering = dict(chain.from_iterable(result))

    if nodes in G:
        return clustering[nodes]
    return clustering
