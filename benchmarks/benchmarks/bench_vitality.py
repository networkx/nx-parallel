from .common import *

class Vitality(Benchmark):
    params = [(algo_types), (num_nodes), (edge_prob)]
    param_names = ["algo_type", "num_nodes", "edge_prob"]

    def time_closeness_vitality(self, algo_type, num_nodes, edge_prob):
        timing_func(get_graph(num_nodes, edge_prob), algo_type, func = nx.closeness_vitality)
