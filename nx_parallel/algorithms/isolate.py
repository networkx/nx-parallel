import networkx as nx
from nx_parallel.partition import NxMap, NxReduce
from nx_parallel.graph import Converters


"""Identical to networkx implementation"""
def is_isolate(G, n):
    return nx.is_isolate(Converters.pargraph2graph(G), n)

"""Identical to networkx implementation"""
def isolates(G):
    return nx.isolates(Converters.pargraph2graph(G))

def number_of_isolates_parallel(G):
    mapped = NxMap(len, iterator="isolate")(G)
    return NxReduce.reduce_partial_solutions(mapped, "sum")
