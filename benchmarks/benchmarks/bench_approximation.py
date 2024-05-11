import networkx as nx

import nx_parallel as nxp

from .common import (
    Benchmark,
    backends,
    edge_prob,
    get_cached_gnp_random_graph,
    num_nodes,
)


class Connectivity(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_approximate_all_pairs_node_connectivity(
        self, backend, num_nodes, edge_prob
    ):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if backend == "parallel":
            G = nxp.ParallelGraph(G)
        _ = nx.algorithms.approximation.connectivity.all_pairs_node_connectivity(G)
