from .common import *
import networkx as nx


class Tournament(Benchmark):
    params = [(backends), (num_nodes)]
    param_names = ["backend", "num_nodes"]

    def time_is_reachable(self, backend, num_nodes):
        G = nx.tournament.random_tournament(num_nodes, seed=42)
        _ = nx.tournament.is_reachable(G, 1, num_nodes, backend=backend)
