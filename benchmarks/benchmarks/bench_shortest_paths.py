from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Generic(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G_weighted = get_cached_gnp_random_graph(
            num_nodes, edge_prob, is_weighted=True
        )

    def time_all_pairs_all_shortest_paths(self, backend, num_nodes, edge_prob):
        _ = dict(
            nx.all_pairs_all_shortest_paths(
                self.G_weighted, weight="weight", backend=backend
            )
        )


class Unweighted(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_all_pairs_shortest_path_length(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_shortest_path_length(self.G, backend=backend))

    def time_all_pairs_shortest_path(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_shortest_path(self.G, backend=backend))


class Weighted(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G_weighted = get_cached_gnp_random_graph(
            num_nodes, edge_prob, is_weighted=True
        )

    def time_all_pairs_dijkstra(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_dijkstra(self.G_weighted, backend=backend))

    def time_all_pairs_dijkstra_path_length(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_dijkstra_path_length(self.G_weighted, backend=backend))

    def time_all_pairs_dijkstra_path(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_dijkstra_path(self.G_weighted, backend=backend))

    def time_all_pairs_bellman_ford_path_length(self, backend, num_nodes, edge_prob):
        _ = dict(
            nx.all_pairs_bellman_ford_path_length(self.G_weighted, backend=backend)
        )

    def time_all_pairs_bellman_ford_path(self, backend, num_nodes, edge_prob):
        _ = dict(nx.all_pairs_bellman_ford_path(self.G_weighted, backend=backend))

    def time_johnson(self, backend, num_nodes, edge_prob):
        _ = nx.johnson(self.G_weighted, backend=backend)
