import networkx as nx
import nx_parallel as nxp


class BetweennessCentralityBenchmark:
    params = [("parallel", "normal")]
    param_names = ["algo_type"]

    def setup(self, algo_type):
        self.algo_type = algo_type

    def time_betweenness_centrality(self, algo_type):
        num_nodes, edge_prob = 300, 0.5
        G = nx.fast_gnp_random_graph(num_nodes, edge_prob, directed=False)
        if algo_type == "parallel":
            H = nxp.ParallelGraph(G)            
            _ = nx.betweenness_centrality(H)
        elif algo_type == "normal":
            _ = nx.betweenness_centrality(G)
        else:
            raise ValueError("Unknown algo_type") 
        