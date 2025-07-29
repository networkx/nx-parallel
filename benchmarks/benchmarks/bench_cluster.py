from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Cluster(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_square_clustering(self, backend, num_nodes, edge_prob):
        _ = nx.square_clustering(self.G, backend=backend)

    def time_triangles(self, backend, num_nodes, edge_prob):
        _ = nx.triangles(self.G, backend=backend)
        
    def time_clustering(self, backend, num_nodes, edge_prob):
        _ = nx.clustering(self.G, backend=backend)
        
    def time_average_clustering(self, backend, num_nodes, edge_prob):
        _ = nx.average_clustering(self.G, backend=backend)
