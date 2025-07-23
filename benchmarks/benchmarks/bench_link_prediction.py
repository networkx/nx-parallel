from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class LinkPrediction(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_resource_allocation_index(self, backend, num_nodes, edge_prob):
        _ = nx.resource_allocation_index(self.G, backend=backend)

    def time_jaccard_coefficient(self, backend, num_nodes, edge_prob):
        _ = nx.jaccard_coefficient(self.G, backend=backend)

    def time_adamic_adar_index(self, backend, num_nodes, edge_prob):
        _ = nx.adamic_adar_index(self.G, backend=backend)

    def time_preferential_attachment(self, backend, num_nodes, edge_prob):
        _ = nx.preferential_attachment(self.G, backend=backend)

    def time_common_neighbor_centrality(self, backend, num_nodes, edge_prob):
        _ = nx.common_neighbor_centrality(self.G, backend=backend)
