from .common import *
import networkx as nx


class EfficiencyMeasures(Benchmark):
    params = [(algo_types), (num_nodes), (edge_prob)]
    param_names = ["algo_type", "num_nodes", "edge_prob"]

    def time_local_efficiency(self, algotype, num_nodes, edge_prob):
        timing_func(get_graph(num_nodes, edge_prob), algotype, func=nx.local_efficiency)
