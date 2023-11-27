from .common import *
import networkx as nx


class Vitality(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_closeness_vitality(self, backend, num_nodes, edge_prob):
        G = cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.closeness_vitality(G, backend=backend)
