from .common import (
    chunking,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import nx_parallel as nxp


class ChunkBenchmarks(Benchmark):
    params = [(chunking), (num_nodes), (edge_prob)]
    param_names = ["chunking", "num_nodes", "edge_prob"]

    def time_betweenness_centrality_chunking(self, chunking, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if chunking:
            _ = nxp.betweenness_centrality_chunk(G)
        else:
            _ = nxp.betweenness_centrality_no_chunk(G)

    def time_all_pairs_bellman_ford_path_chunking(self, chunking, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob, is_weighted=True)
        if chunking:
            _ = dict(nxp.all_pairs_bellman_ford_path_chunk(G))
        else:
            _ = dict(nxp.all_pairs_bellman_ford_path_no_chunk(G))

    def time_local_efficiency_chunking(self, chunking, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if chunking:
            _ = nxp.local_efficiency_chunk(G)
        else:
            _ = nxp.local_efficiency_no_chunk(G)

    def time_number_of_isolates_chunking(self, chunking, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if chunking:
            _ = nxp.number_of_isolates_chunk(G)
        else:
            _ = nxp.number_of_isolates_no_chunk(G)

    def time_closeness_vitality_chunking(self, chunking, num_nodes, edge_prob):
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        if chunking:
            _ = nxp.closeness_vitality_chunk(G)
        else:
            _ = nxp.closeness_vitality_no_chunk(G)
