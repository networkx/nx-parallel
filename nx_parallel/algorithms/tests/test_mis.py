import networkx as nx
import nx_parallel as nxp
import pytest


def test_maximal_independent_set_basic():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    result = nxp.maximal_independent_set(H)

    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)

    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            assert result_set.intersection(neighbors)


def test_maximal_independent_set_with_required_nodes():
    G = nx.path_graph(7)
    H = nxp.ParallelGraph(G)
    required_nodes = [1, 3]
    result = nxp.maximal_independent_set(H, nodes=required_nodes)

    assert 1 in result
    assert 3 in result

    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)


def test_maximal_independent_set_invalid_nodes():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)

    with pytest.raises(nx.NetworkXUnfeasible):
        nxp.maximal_independent_set(H, nodes=[10, 20])

    with pytest.raises(nx.NetworkXUnfeasible):
        nxp.maximal_independent_set(H, nodes=[0, 1])


def test_maximal_independent_set_directed_graph():
    G = nx.DiGraph([(0, 1), (1, 2)])
    H = nxp.ParallelGraph(G)

    with pytest.raises(nx.NetworkXNotImplemented):
        nxp.maximal_independent_set(H)


def test_maximal_independent_set_deterministic_with_seed():
    G = nx.karate_club_graph()
    H = nxp.ParallelGraph(G)

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=42)

    assert result1 == result2


def test_maximal_independent_set_different_seeds():
    G = nx.karate_club_graph()
    H = nxp.ParallelGraph(G)

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=100)

    for result in [result1, result2]:
        result_set = set(result)
        for node in result:
            neighbors = set(G.neighbors(node))
            assert not result_set.intersection(neighbors)


def test_maximal_independent_set_complete_graph():
    G = nx.complete_graph(5)
    H = nxp.ParallelGraph(G)
    result = nxp.maximal_independent_set(H)

    assert len(result) == 1


def test_maximal_independent_set_empty_graph():
    G = nx.empty_graph(5)
    H = nxp.ParallelGraph(G)
    result = nxp.maximal_independent_set(H)

    assert len(result) == 5


def test_maximal_independent_set_large_graph():
    G = nx.fast_gnp_random_graph(150, 0.1, seed=42)
    H = nxp.ParallelGraph(G)
    result = nxp.maximal_independent_set(H, seed=42)

    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)

    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            assert result_set.intersection(neighbors)


def test_maximal_independent_set_random_graph():
    G = nx.fast_gnp_random_graph(50, 0.1, seed=42)
    H = nxp.ParallelGraph(G)
    result = nxp.maximal_independent_set(H, seed=42)

    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)

    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            assert result_set.intersection(neighbors)
