from .common import (
    backends,
    num_nodes,
    edge_prob,
    get_cached_gnp_random_graph,
    Benchmark,
)
import nx_parallel as nxp


class HarmonicCentrality(Benchmark):
    """Benchmark for the parallelized Harmonic Centrality computation."""

    params = [(backends), (num_nodes), (edge_prob)]
    param_names = ["backend", "num_nodes", "edge_prob"]

    def time_harmonic_centrality(self, backend, num_nodes, edge_prob):
        """Benchmark Harmonic Centrality on different graph sizes and backends."""
        G = get_cached_gnp_random_graph(num_nodes, edge_prob)
        _ = nxp.harmonic_centrality(G, backend=backend)
