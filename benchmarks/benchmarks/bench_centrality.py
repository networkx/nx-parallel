from .common import *

class BetweennessCentralityBenchmark(Benchmark):
    params = [
        (algo_types),
        (num_nodes),
        (edge_prob)
    ]
    param_names = ["algo_type","num_nodes","edge_prob"]

    def time_betweenness_centrality(self, algo_type, num_nodes, edge_prob):
        G = get_graph(num_nodes, edge_prob)
        standard_timing_func(G, algo_type, func = nx.betweenness_centrality)
