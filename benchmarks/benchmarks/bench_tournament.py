from .common import (
    backends,
    num_nodes,
    Benchmark,
)
import networkx as nx


class Tournament(Benchmark):
    params = [(backends), (num_nodes)]
    param_names = ["backend", "num_nodes"]

    def time_is_reachable(self, backend, num_nodes):
        G = nx.tournament.random_tournament(num_nodes, seed=42)
        _ = nx.tournament.is_reachable(G, 1, num_nodes, backend=backend)

    def time_tournament_is_strongly_connected(self, backend, num_nodes):
        G = nx.tournament.random_tournament(num_nodes, seed=42)
        _ = nx.tournament.is_strongly_connected(G, backend=backend)
