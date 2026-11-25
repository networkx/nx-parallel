import math

import networkx as nx
import pytest

import nx_parallel as nxp


def test_global_efficiency_empty_and_single_node():
    for G in (nx.Graph(), nx.empty_graph(1), nx.MultiGraph()):
        assert nxp.global_efficiency(G) == 0
        assert nx.global_efficiency(G, backend="parallel") == 0


def test_global_efficiency_matches_networkx():
    graphs = [
        nx.cycle_graph(4),
        nx.complete_graph(6),
        nx.lollipop_graph(3, 2),
        nx.path_graph(10),
        nx.empty_graph(5),
        nx.fast_gnp_random_graph(40, 0.3, seed=42),
        nx.MultiGraph([(0, 1), (0, 1), (1, 2), (2, 3)]),
    ]
    for G in graphs:
        expected = nx.global_efficiency(G)
        H = nxp.ParallelGraph(G)
        assert math.isclose(nxp.global_efficiency(G), expected, abs_tol=1e-15)
        assert math.isclose(nxp.global_efficiency(H), expected, abs_tol=1e-15)
        assert math.isclose(
            nx.global_efficiency(G, backend="parallel"), expected, abs_tol=1e-15
        )
        assert math.isclose(nx.global_efficiency(H), expected, abs_tol=1e-15)


def test_global_efficiency_directed_raises():
    D = nx.DiGraph([(0, 1), (1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        nxp.global_efficiency(D)
    with pytest.raises(nx.NetworkXNotImplemented):
        nxp.global_efficiency(nxp.ParallelGraph(D))
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.global_efficiency(D, backend="parallel")


def test_global_efficiency_get_chunks():
    G = nx.fast_gnp_random_graph(30, 0.4, seed=7)
    H = nxp.ParallelGraph(G)

    def custom_chunks(nodes):
        node_list = list(nodes)
        mid = len(node_list) // 2
        return [node_list[:mid], node_list[mid:]]

    expected = nx.global_efficiency(G)
    result = nxp.global_efficiency(H, get_chunks=custom_chunks)
    assert math.isclose(result, expected, abs_tol=1e-15)
