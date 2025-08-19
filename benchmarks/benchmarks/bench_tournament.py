from .common import (
    backends,
    num_nodes,
    seed,
    Benchmark,
)
import networkx as nx
import random


class Tournament(Benchmark):
    params = [backends, num_nodes]
    param_names = ["backend", "num_nodes"]

    def setup(self, backend, num_nodes):
        self.G = nx.tournament.random_tournament(num_nodes, seed=seed)
        self.nodes = sorted(self.G)
        rng = random.Random(seed)
        self.source, self.target = rng.sample(self.nodes, 2)

    def time_is_reachable(self, backend, num_nodes):
        _ = nx.tournament.is_reachable(
            self.G, self.source, self.target, backend=backend
        )

    def time_tournament_is_strongly_connected(self, backend, num_nodes):
        _ = nx.tournament.is_strongly_connected(self.G, backend=backend)
