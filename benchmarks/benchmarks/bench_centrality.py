from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Betweenness(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        self.G_weighted = get_cached_gnp_random_graph(
            num_nodes, edge_prob, is_weighted=True
        )

    def time_betweenness_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.betweenness_centrality(self.G, backend=backend)

    def time_edge_betweenness_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.edge_betweenness_centrality(self.G_weighted, backend=backend)
