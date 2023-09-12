"""Unit tests for the :mod:`networkx.algorithms.isolates` module. Modified for nx_parallel backend"""

import networkx as nx

import nx_parallel


def test_is_isolate():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_node(2)
    H = nx_parallel.ParallelGraph(G)
    assert not nx.is_isolate(H, 0)
    assert not nx.is_isolate(H, 1)
    assert nx.is_isolate(H, 2)


def test_isolates():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_nodes_from([2, 3])
    H = nx_parallel.ParallelGraph(G)
    assert sorted(nx.isolates(H)) == [2, 3]


def test_number_of_isolates():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_nodes_from([2, 3])
    H = nx_parallel.ParallelGraph(G)
    assert nx.number_of_isolates(H) == 2
