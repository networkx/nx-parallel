from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Cluster(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_square_clustering(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.square_clustering(G, backend=backend)
