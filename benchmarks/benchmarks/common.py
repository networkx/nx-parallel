from functools import lru_cache
from pathlib import Path
import types
import random

import networkx as nx
import nx_parallel as nxp


CACHE_ROOT = Path(__file__).resolve().parent.parent / "env" / "nxp_benchdata"

algo_types = ["parallel", "sequential"]
num_nodes = [50, 100, 200, 400, 800]
edge_prob = [0.8, 0.6, 0.4, 0.2]


@lru_cache(typed=True)
def get_graph(num_nodes, edge_prob, is_weighted=False):
    G = nx.fast_gnp_random_graph(num_nodes, edge_prob, seed=42, directed=False)
    if is_weighted:
        random.seed(42)
        for (u, v) in G.edges():
            G.edges[u, v]["weight"] = random.random()
    return G


def timing_func(G, algo_type, func, *args, **kwargs):
    if algo_type == "parallel":
        H = nxp.ParallelGraph(G)
        _ = func(H, *args, **kwargs)
        if type(_) == types.GeneratorType:
            d = dict(_)
    elif algo_type == "sequential":
        _ = func(G, *args, **kwargs)
        if type(_) == types.GeneratorType:
            d = dict(_)
    # if you want to use the following, then pls add "using_kwargs" in `algo_types` above in line 12
    # elif algo_type == "using_kwargs":
    #    _ = func(G, *args, **kwargs, backend='parallel')
    #    if type(_)==types.GeneratorType: d = dict(_)
    else:
        raise ValueError("Unknown algo_type")


class Benchmark:
    pass
