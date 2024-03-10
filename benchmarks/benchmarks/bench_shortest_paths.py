from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Weighted(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_all_pairs_bellman_ford_path(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob, is_weighted=True)
        _ = dict(nx.all_pairs_bellman_ford_path(G, backend=backend))

    def time_johnson(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob, is_weighted=True)
        _ = nx.johnson(G, backend=backend)
