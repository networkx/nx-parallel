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
        self.G_community = self.G.copy()
        for i, node in enumerate(self.G_community.nodes()):
            self.G_community.nodes[node]["community"] = i % 4

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

    def time_cn_soundarajan_hopcroft(self, backend, num_nodes, edge_prob):
        _ = nx.cn_soundarajan_hopcroft(self.G_community, backend=backend)

    def time_ra_index_soundarajan_hopcroft(self, backend, num_nodes, edge_prob):
        _ = nx.ra_index_soundarajan_hopcroft(self.G_community, backend=backend)

    def time_within_inter_cluster(self, backend, num_nodes, edge_prob):
        _ = nx.within_inter_cluster(self.G_community, backend=backend)
