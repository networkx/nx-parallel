from typing import ClassVar

import networkx as nx

from .common import (
    Benchmark,
    backends,
    edge_prob,
    seed,
)

# for an unbalanced bipartite random graph
n = [50, 100, 200, 400, 800]
m = [25, 50, 100, 200, 400]


class Redundancy(Benchmark):
    params: ClassVar[list] = [backends, n, m, edge_prob]
    param_names: ClassVar[list] = ["backend", "n", "m", "edge_prob"]

    def setup(self, backend, n, m, edge_prob):
        self.G = get_random_bipartite_graph(n, m, edge_prob)

    def time_node_redundancy(self, backend, n, m, edge_prob):
        _ = nx.node_redundancy(self.G, backend=backend)


def get_random_bipartite_graph(n, m, edge_prob, directed=False):
    """Ref. https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.generators.random_graph.html"""
    return nx.bipartite.random_graph(n, m, edge_prob, seed, directed)
