from typing import ClassVar

import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class Assortativity(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_average_neighbor_degree(self, backend, num_nodes, edge_prob):
        _ = nx.average_neighbor_degree(self.G, backend=backend)
