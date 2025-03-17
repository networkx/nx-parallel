import networkx as nx
import nx_parallel as nxp
from asv_bench.benchmarks.utils import benchmark


class BenchmarkVoteRank:
    """Benchmark for the voterank algorithm in nx_parallel."""

    def setup(self):
        """Set up test graphs before running the benchmarks."""
        self.G_small = nx.erdos_renyi_graph(100, 0.1, seed=42)
        self.G_medium = nx.erdos_renyi_graph(1000, 0.05, seed=42)
        self.G_large = nx.erdos_renyi_graph(5000, 0.01, seed=42)

    @benchmark.benchmark
    def time_voterank_small(self):
        """Benchmark VoteRank on a small graph."""
        nxp.voterank(self.G_small, number_of_nodes=10)

    @benchmark.benchmark
    def time_voterank_medium(self):
        """Benchmark VoteRank on a medium graph."""
        nxp.voterank(self.G_medium, number_of_nodes=50)

    @benchmark.benchmark
    def time_voterank_large(self):
        """Benchmark VoteRank on a large graph."""
        nxp.voterank(self.G_large, number_of_nodes=100)
