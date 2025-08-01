from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx
import nx_parallel as nxp


class Assortativity(Benchmark):
    params = [backends, num_nodes, edge_prob]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def setup(self, backend, num_nodes, edge_prob):
        self.G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if backend == "parallel":
            self.G = nxp.ParallelGraph(self.G)

    def time_average_neighbor_degree(self, backend, num_nodes, edge_prob):
        _ = nx.average_neighbor_degree(self.G)
