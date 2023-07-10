from joblib import Parallel, cpu_count, delayed
import networkx as nx
from nx_parallel.algorithms.utils.chunk import chunks
from nx_parallel.classes.graph import ParallelGraph, ParallelDiGraph,ParallelMultiDiGraph, ParallelMultiGraph

__all__ = ["number_of_isolates"]

"""Helper to interface between graph types"""
def _convert(G):
    if isinstance(G, ParallelMultiDiGraph):
        I = ParallelMultiDiGraph.to_networkx(G)
    if isinstance(G, ParallelMultiGraph):
        I = ParallelMultiGraph.to_networkx(G)
    if isinstance(G, ParallelDiGraph):
        I = ParallelDiGraph.to_networkx(G)
    if isinstance(G, ParallelGraph):
        I = ParallelGraph.to_networkx(G)
    return I

"""Identical to networkx implementation"""
def is_isolate(G, n):
    return nx.is_isolate(_convert(G), n)

"""Identical to networkx implementation"""
def isolates(G):
    return nx.isolates(_convert(G))
    
def number_of_isolates(G):
    """Returns the number of isolates in the graph. Parallel implementation.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    """
    isolates_list = list(isolates(G))
    num_chunks = max(len(isolates_list) // cpu_count(), 1)
    isolate_chunks = chunks(isolates_list, num_chunks)
    results = Parallel(n_jobs=-1)(delayed(len)(chunk) for chunk in isolate_chunks)
    return sum(results)



