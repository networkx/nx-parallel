from .common import *
import networkx as nx


def get_tournament_graph(num, seed=42):
    return nx.tournament.random_tournament(num, seed=seed)


class Tournament(Benchmark):
    params = [(algo_types), (num_nodes)]
    param_names = ["algo_type", "num_nodes"]

    def time_is_reachable(self, algo_type, num_nodes):
        G = get_tournament_graph(num_nodes)
        timing_func(G, algo_type, nx.tournament.is_reachable, 1, num_nodes)
