from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class EfficiencyMeasures(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_local_efficiency(self, backend, num_nodes, edge_prob):
        _ = nx.local_efficiency(self.G, backend=backend)
