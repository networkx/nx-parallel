from functools import lru_cache
from pathlib import Path
import random

import networkx as nx

__all__ = [
    "backends",
    "num_nodes",
    "edge_prob",
    "get_cached_gnp_random_graph",
    "Benchmark",
]

CACHE_ROOT = Path(__file__).resolve().parent.parent / "env" / "nxp_benchdata"

backends = ["parallel", None]
num_nodes = [50, 100, 200, 400, 800]
edge_prob = [0.8, 0.6, 0.4, 0.2]
seed = 42


@lru_cache(typed=True)
def get_cached_gnp_random_graph(
    num_nodes, edge_prob, is_weighted=False, is_directed=False
):
    G = nx.fast_gnp_random_graph(num_nodes, edge_prob, seed=seed, directed=is_directed)
    if is_weighted:
        random.seed(seed)
        for u, v in G.edges():
            G.edges[u, v]["weight"] = random.random()
    return G


class Benchmark:
    pass
