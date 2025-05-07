from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import nx_parallel as nxp


class VoteRank(Benchmark):
    """Benchmark for the parallelized VoteRank centrality."""

    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_voterank(self, backend, num_nodes, edge_prob):
        """Benchmark VoteRank on different graph sizes and backends."""
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nxp.voterank(G, number_of_nodes=min(100, num_nodes), backend=backend)
