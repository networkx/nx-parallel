from .common import chunking, num_nodes, Benchmark
import nx_parallel as nxp
import networkx as nx


class TournamentChunkBenchmark(Benchmark):
    params = [(chunking), (num_nodes)]
    param_names = ["chunking", "num_nodes"]

    def time_tournament_is_reachable_chunking(self, chunking, num_nodes):
        G = nx.tournament.random_tournament(num_nodes, seed=42)
        if chunking:
            _ = nxp.tournament.is_reachable_chunk(G, 1, num_nodes)
        else:
            _ = nxp.tournament.is_reachable_no_chunk(G, 1, num_nodes)

    def time_tournament_is_strongly_connected_chunking(self, chunking, num_nodes):
        G = nx.tournament.random_tournament(num_nodes, seed=42)
        if chunking:
            _ = nxp.tournament.is_strongly_connected_chunk(G)
        else:
            _ = nxp.tournament.is_strongly_connected_no_chunk(G)
