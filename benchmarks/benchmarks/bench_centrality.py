import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class Betweenness(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_betweenness_centrality(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.betweenness_centrality(G, backend=backend)
