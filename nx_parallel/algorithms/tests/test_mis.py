import networkx as nx
import nx_parallel as nxp
import pytest


def test_maximal_independent_set_basic():
    """Test basic functionality of parallel maximal_independent_set."""
    # Test on a simple path graph
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)

    # Get result from parallel version
    result = nxp.maximal_independent_set(H)

    # Verify it's a valid independent set
    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors), "Independent set constraint violated"

    # Verify it's maximal (no node can be added)
    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            # At least one neighbor must be in the independent set
            assert result_set.intersection(neighbors), f"Set is not maximal, could add node {node}"


def test_maximal_independent_set_with_required_nodes():
    """Test maximal_independent_set with required nodes."""
    G = nx.path_graph(7)
    H = nxp.ParallelGraph(G)

    # Require nodes 1 and 3 (they are not adjacent in path graph)
    required_nodes = [1, 3]
    result = nxp.maximal_independent_set(H, nodes=required_nodes)

    # Verify required nodes are in result
    assert 1 in result, "Required node 1 not in result"
    assert 3 in result, "Required node 3 not in result"

    # Verify it's a valid independent set
    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors), "Independent set constraint violated"


def test_maximal_independent_set_invalid_nodes():
    """Test that invalid required nodes raise exception."""
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)

    # Test with nodes that are not in graph
    with pytest.raises(nx.NetworkXUnfeasible):
        nxp.maximal_independent_set(H, nodes=[10, 20])

    # Test with nodes that are adjacent (not independent)
    with pytest.raises(nx.NetworkXUnfeasible):
        nxp.maximal_independent_set(H, nodes=[0, 1])


def test_maximal_independent_set_directed_graph():
    """Test that directed graphs raise exception."""
    G = nx.DiGraph([(0, 1), (1, 2)])
    H = nxp.ParallelGraph(G)

    with pytest.raises(nx.NetworkXNotImplemented):
        nxp.maximal_independent_set(H)


def test_maximal_independent_set_deterministic_with_seed():
    """Test that results are deterministic with same seed."""
    G = nx.karate_club_graph()
    H = nxp.ParallelGraph(G)

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=42)

    # Results should be identical with same seed
    assert result1 == result2, "Results with same seed should be identical"


def test_maximal_independent_set_different_seeds():
    """Test that different seeds can produce different results."""
    G = nx.karate_club_graph()
    H = nxp.ParallelGraph(G)

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=100)

    # Both should be valid maximal independent sets
    for result in [result1, result2]:
        result_set = set(result)
        for node in result:
            neighbors = set(G.neighbors(node))
            assert not result_set.intersection(neighbors)


def test_maximal_independent_set_complete_graph():
    """Test on complete graph (only one node can be in independent set)."""
    G = nx.complete_graph(5)
    H = nxp.ParallelGraph(G)

    result = nxp.maximal_independent_set(H)

    # Complete graph should have exactly one node in maximal independent set
    assert len(result) == 1, f"Complete graph should have exactly 1 node in MIS, got {len(result)}"


def test_maximal_independent_set_empty_graph():
    """Test on empty graph (no edges)."""
    G = nx.empty_graph(5)
    H = nxp.ParallelGraph(G)

    result = nxp.maximal_independent_set(H)

    # Empty graph should have all nodes in maximal independent set
    assert len(result) == 5, f"Empty graph should have all 5 nodes in MIS, got {len(result)}"


def test_maximal_independent_set_large_graph():
    """Test on larger graph for parallel processing."""
    G = nx.fast_gnp_random_graph(150, 0.1, seed=42)
    H = nxp.ParallelGraph(G)

    # Test on larger graph where parallelization kicks in
    result = nxp.maximal_independent_set(H, seed=42)

    # Should be a valid maximal independent set
    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)

    # Verify maximality
    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            assert result_set.intersection(neighbors)


def test_maximal_independent_set_random_graph():
    """Test on random graph for robustness."""
    G = nx.fast_gnp_random_graph(50, 0.1, seed=42)
    H = nxp.ParallelGraph(G)

    result = nxp.maximal_independent_set(H, seed=42)

    # Verify it's a valid maximal independent set
    result_set = set(result)
    for node in result:
        neighbors = set(G.neighbors(node))
        assert not result_set.intersection(neighbors)

    # Verify maximality
    for node in G.nodes():
        if node not in result_set:
            neighbors = set(G.neighbors(node))
            assert result_set.intersection(neighbors)
