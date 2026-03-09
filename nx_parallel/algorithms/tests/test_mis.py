import networkx as nx
import nx_parallel as nxp


def test_should_run_small_graph():
    """Small graphs should fall back to NetworkX sequential implementation."""
    G = nx.fast_gnp_random_graph(100, 0.1, seed=42)
    H = nxp.ParallelGraph(G)

    result = nxp.maximal_independent_set.should_run(H)
    assert result == "Graph too small for parallel execution"


def test_should_run_large_graph():
    """Large graphs should use the parallel implementation."""
    G = nx.fast_gnp_random_graph(60000, 0.0001, seed=42)
    H = nxp.ParallelGraph(G)

    result = nxp.maximal_independent_set.should_run(H)
    assert result is True


def test_get_chunks():
    """Test custom chunking function."""
    G = nx.fast_gnp_random_graph(60000, 0.0001, seed=42)
    H = nxp.ParallelGraph(G)

    def custom_chunks(nodes):
        nodes_list = list(nodes)
        mid = len(nodes_list) // 2
        return [nodes_list[:mid], nodes_list[mid:]]

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=42, get_chunks=custom_chunks)

    # Both should be valid independent sets (correctness is tested by NetworkX)
    for result in [result1, result2]:
        result_set = set(result)
        for node in result:
            neighbors = set(G.neighbors(node))
            assert not result_set.intersection(neighbors)


def test_parallel_deterministic_with_seed():
    """Parallel execution with same seed should produce same result."""
    G = nx.fast_gnp_random_graph(60000, 0.0001, seed=42)
    H = nxp.ParallelGraph(G)

    result1 = nxp.maximal_independent_set(H, seed=42)
    result2 = nxp.maximal_independent_set(H, seed=42)

    assert result1 == result2
