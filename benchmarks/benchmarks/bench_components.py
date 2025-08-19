from .common import (
    backends,
    num_nodes,
    edge_prob,
    seed,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Attracting(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_attracting_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_attracting_components(self.G, backend=backend)


class Connected(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_number_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_connected_components(self.G, backend=backend)


class StronglyConnected(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_strongly_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_strongly_connected_components(self.G, backend=backend)


class WeaklyConnected(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(
            num_nodes, edge_prob, seed=seed, is_directed=True
        )

    def time_number_weakly_connected_components(self, backend, num_nodes, edge_prob):
        _ = nx.number_weakly_connected_components(self.G, backend=backend)
