from itertools import combinations
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["square_clustering"]


def square_clustering(G, nodes=None):
    """The squares clustering coefficient for nodes for all nodes
    are computed in parallel over all available CPU cores.

    networkx.square_clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.square_clustering.html
    """

    def _compute_clustering(v):
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
        return (v, clustering)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if nodes is None:
        node_iter = G
    else:
        node_iter = G.nbunch_iter(nodes)

    total_cores = nxp.cpu_count()

    result = Parallel(n_jobs=total_cores)(
        delayed(_compute_clustering)(v) for v in node_iter
    )
    clustering = dict(result)

    if nodes in G:
        return clustering[nodes]
    return clustering
