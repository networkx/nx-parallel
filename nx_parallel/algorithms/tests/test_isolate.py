"""Unit tests for the :mod:`networkx.algorithms.isolates` module. Modified for nx_parallel backend"""

import networkx as nx

import nx_parallel


def test_number_of_isolates():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_nodes_from([2, 3])
    H = nx_parallel.ParallelGraph(G)
    assert nx.number_of_isolates(H) == 2
