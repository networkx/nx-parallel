from typing import ClassVar

import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class Isolate(Benchmark):
    params: ClassVar[list] = [backends, num_nodes, edge_prob]
    param_names: ClassVar[list] = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)

    def time_number_of_isolates(self, backend, num_nodes, edge_prob):
        _ = nx.number_of_isolates(self.G, backend=backend)
