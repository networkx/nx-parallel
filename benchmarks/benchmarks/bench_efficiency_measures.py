from .common import *
import networkx as nx


class EfficiencyMeasures(Benchmark):
    params = [(algo_types), (num_nodes), (edge_prob)]
    param_names = ["algo_type", "num_nodes", "edge_prob"]

    def time_local_efficiency(self, algo_type, num_nodes, edge_prob):
        timing_func(get_graph(num_nodes, edge_prob), algo_type, func=nx.local_efficiency)
