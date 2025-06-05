from itertools import combinations, chain
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "square_clustering",
]


@nxp._configure_if_nx_active()
def square_clustering(G, nodes=None, get_chunks="chunks"):
    """The nodes are chunked into `node_chunks` and then the square clustering
    coefficient for all `node_chunks` are computed in parallel over `n_jobs` number
    of CPU cores.

    networkx.square_clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.square_clustering.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _compute_clustering_chunk(node_iter_chunk):
        result_chunk = []
        for v in node_iter_chunk:
            clustering = 0
            potential = 0
            v_nbrs = G_nbrs_as_sets[v]
            for u, w in combinations(v_nbrs, 2):
                u_nbrs = G_nbrs_as_sets[u]
                w_nbrs = G_nbrs_as_sets[w]
                squares = len((u_nbrs & w_nbrs) - {v})
                clustering += squares
                degm = squares + 1
                if w in u_nbrs:
                    degm += 1
                potential += (len(u_nbrs) - degm) + (len(w_nbrs) - degm) + squares
            if potential > 0:
                clustering /= potential
            result_chunk += [(v, clustering)]
        return result_chunk

    if hasattr(G, "graph_object"):
        G = G.graph_object

    # ignore self-loops as per networkx 3.5
    G_nbrs_as_sets = {node: set(G[node]) - {node} for node in G}

    if nodes is None:
        node_iter = list(G)
    else:
        node_iter = list(G.nbunch_iter(nodes))

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_iter_chunks = nxp.chunks(node_iter, n_jobs)
    else:
        node_iter_chunks = get_chunks(node_iter)

    result = Parallel()(
        delayed(_compute_clustering_chunk)(node_iter_chunk)
        for node_iter_chunk in node_iter_chunks
    )
    clustering = dict(chain.from_iterable(result))

    if nodes in G:
        return clustering[nodes]
    return clustering
