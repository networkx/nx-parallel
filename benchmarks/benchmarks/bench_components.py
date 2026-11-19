from typing import ClassVar

import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
    seed,
)


class Attracting(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_attracting_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_attracting_components(self.G, backend=backend)


class Connected(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_number_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_connected_components(self.G, backend=backend)


class StronglyConnected(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_strongly_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_strongly_connected_components(self.G, backend=backend)


class WeaklyConnected(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_weakly_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_weakly_connected_components(self.G, backend=backend)
