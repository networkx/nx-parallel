from .common import *
import networkx as nx


class Isolate(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_number_of_isolates(self, backend, num_nodes, edge_prob):
        G = cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.number_of_isolates(G, backend=backend)
