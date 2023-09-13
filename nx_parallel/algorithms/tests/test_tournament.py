"""Unit tests for the :mod:`networkx.algorithms.tournament` module. Modified for nx_parallel backend"""
from itertools import combinations

import pytest
from networkx import DiGraph
from networkx.algorithms.tournament import is_reachable, is_strongly_connected

import nx_parallel as nxp


def test_reachable_pair():
    """Tests for a reachable pair of nodes."""
    G = DiGraph([(0, 1), (1, 2), (2, 0)])
    H = nxp.ParallelGraph(G)
    assert is_reachable(H, 0, 2)


def test_same_node_is_reachable():
    """Tests that a node is always reachable from it."""
    # G is an arbitrary tournament on ten nodes.
    G = DiGraph(sorted(p) for p in combinations(range(10), 2))
    H = nxp.ParallelGraph(G)
    assert all(is_reachable(H, v, v) for v in G)


def test_unreachable_pair():
    """Tests for an unreachable pair of nodes."""
    G = DiGraph([(0, 1), (0, 2), (1, 2)])
    H = nxp.ParallelGraph(G)
    assert not is_reachable(H, 1, 0)


def test_is_strongly_connected():
    """Tests for a strongly connected tournament."""
    G = DiGraph([(0, 1), (1, 2), (2, 0)])
    H = nxp.ParallelGraph(G)
    assert is_strongly_connected(H)


def test_not_strongly_connected():
    """Tests for a tournament that is not strongly connected."""
    G = DiGraph([(0, 1), (0, 2), (1, 2)])
    H = nxp.ParallelGraph(G)
    assert not is_strongly_connected(H)


def test_doc_examples_outside_doc_string():
    G = nx.DiGraph([(1, 0), (1, 3), (1, 2), (2, 3), (2, 0), (3, 0)])
    H = nxp.ParallelGraph(G)
    assert nx.tournament.is_tournament(G)
    assert nx.tournament.is_reachable(H, 1, 3)
    assert nx.tournament.is_reachable(G, 1, 3, backend="parallel")
    assert not nx.tournament.is_reachable(H, 3, 2)
    assert not nx.tournament.is_reachable(G, 3, 2, backend="parallel")
