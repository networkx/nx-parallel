from functools import lru_cache
from pathlib import Path

import networkx as nx
import nx_parallel as nxp


CACHE_ROOT = Path(__file__).resolve().parent.parent / 'env' / 'nxp_benchdata'

algo_types = ["parallel", "sequential"]
num_nodes = [10, 50, 100, 300, 500]
edge_prob = [1, 0.8, 0.6, 0.4, 0.2]

@lru_cache(typed=True)
def get_graph(num_nodes, edge_prob):
    G = nx.fast_gnp_random_graph(num_nodes, edge_prob, seed=42, directed=False)
    return G

def standard_timing_func(G, algo_type, func):
    if algo_type == "parallel":
        H = nxp.ParallelGraph(G)            
        _ = func(H)
    elif algo_type == "sequential":
        _ = func(G)
    # if you want to use this then pls add "using_backend" in algo_types above in line 10
    #elif algo_type == "using_backend": 
    #    _ = func(G, backend='parallel')
    else:
        raise ValueError("Unknown algo_type") 


class Benchmark:
    pass
