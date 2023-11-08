from .common import *

class BetweennessCentrality(Benchmark):
    params = [(algo_types),
              (num_nodes), 
              (edge_prob)
             ]
    param_names = ["algo_type", "num_nodes", "edge_prob"]

    def time_betweenness_centrality(self, algo_type, num_nodes, edge_prob):
        timing_func(get_graph(num_nodes, edge_prob), algo_type, func = nx.betweenness_centrality)
