from .common import (
    backends,
    edge_prob,
    Benchmark,
)
import networkx as nx

# for an unbalanced bipartite random graph
n = [50, 100, 200, 400, 800]
m = [25, 50, 100, 200, 400]


class Redundancy(Benchmark):
    params = [(backends), (n), (m), (edge_prob)]
    param_names = ["backend", "n", "m", "edge_prob"]

    def time_node_redundancy(self, backend, n, m, edge_prob):
        G = get_random_bipartite_graph(n, m, edge_prob)
        _ = nx.node_redundancy(G, backend=backend)


def get_random_bipartite_graph(n, m, p, seed=42, directed=False):
    """Ref. https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.generators.random_graph.html"""
    return nx.bipartite.random_graph(n, m, p, seed, directed)
