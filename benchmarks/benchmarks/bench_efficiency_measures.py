import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class EfficiencyMeasures(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_local_efficiency(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.local_efficiency(G, backend=backend)
