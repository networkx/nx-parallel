from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import networkx as nx
import random


class Betweenness(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_betweenness_centrality(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nx.betweenness_centrality(G, backend=backend)


class Reaching(Benchmark):
    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_global_reaching_centrality(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob, is_weighted=True, directed=True)
        _ = nx.global_reaching_centrality(G, weight="weight", backend=backend)

    def time_local_reaching_centrality(self, backend, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob, is_weighted=True, directed=True)
        random.seed(42)
        v = random.randint(0, num_nodes-1)
        _ = nx.local_reaching_centrality(G, v, weight="weight", backend=backend)
