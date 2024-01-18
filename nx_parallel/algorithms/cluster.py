from itertools import combinations
from joblib import Parallel, delayed

__all__ = ["square_clustering"]


def square_clustering(G, nodes=None):
    def _compute_clustering(v):
        def _process_edge(edge):
            nonlocal clustering, potential
            u, w = edge
            squares = len((set(G[u]) & set(G[w])) - {v})
            clustering += squares
            degm = squares + 1
            if w in G[u]:
                degm += 1
            potential += (len(G[u]) - degm) + (len(G[w]) - degm) + squares

        clustering = 0
        potential = 0
        edges = combinations(G[v], 2)
        Parallel(n_jobs=-1)(delayed(_process_edge)(edge) for edge in edges)

        if potential > 0:
            clustering /= potential
        return v, clustering

    if nodes is None:
        node_iter = G.nodes()
    else:
        node_iter = G.nbunch_iter(nodes)

    clustering = dict(
        Parallel(n_jobs=-1)(delayed(_compute_clustering)(v) for v in node_iter)
    )

    if nodes in G:
        return clustering[nodes]
    return clustering
