from typing import ClassVar

import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class Betweenness(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        self.G_weighted = get_cached_gnp_random_graph(
            num_nodes, edge_prob, is_weighted=True
        )

    def time_betweenness_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.betweenness_centrality(self.G, backend=backend)

    def time_edge_betweenness_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.edge_betweenness_centrality(self.G_weighted, backend=backend)


class Harmonic(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_harmonic_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.harmonic_centrality(self.G, backend=backend)
