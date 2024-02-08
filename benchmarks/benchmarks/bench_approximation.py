from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx


class Connectivity(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_all_pairs_node_connectivity(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = dict(nx.all_pairs_node_connectivity(G, backend=backend))
