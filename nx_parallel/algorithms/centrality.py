import networkx as nx
from nx_parallel.partition import NxMap, NxReduce
from nx_parallel.graph import Converters

def betweenness_centrality_parallel(G):
    mapped = NxMap(nx.betweenness_centrality_subset, iterator="node")(Converters.graph2pargraph(G))
    return NxReduce.reduce_partial_solutions(mapped, "concatenate")

def edge_betweenness_centrality_parallel(G):
    mapped = NxMap(nx.edge_betweenness_centrality_subset, iterator="edge")(Converters.graph2pargraph(G))
    return NxReduce.reduce_partial_solutions(mapped, "concatenate")