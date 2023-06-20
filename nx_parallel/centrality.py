from joblib import Parallel, delayed
from networkx.algorithms.centrality.betweenness import (
    _single_source_shortest_path_basic,
    _accumulate_endpoints,
    _accumulate_basic,
    _rescale,
    _single_source_dijkstra_path_basic,
)

__all__ = ["betweenness_centrality"]


def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    if k is None:
        nodes = G
    else:
        nodes = seed.sample(list(G.nodes()), k)

    def __node_loop(nodes):
        for s in nodes:
            # single source shortest paths
            if weight is None:  # use BFS
                S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
            else:  # use Dijkstra's algorithm
                S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)
            # accumulation
            if endpoints:
                betweenness, _ = _accumulate_endpoints(betweenness, S, P, sigma, s)
            else:
                betweenness, _ = _accumulate_basic(betweenness, S, P, sigma, s)

    # rescaling
    betweenness = _rescale(
        betweenness,
        len(G),
        normalized=normalized,
        directed=G.is_directed(),
        k=k,
        endpoints=endpoints,
    )
    return betweenness
