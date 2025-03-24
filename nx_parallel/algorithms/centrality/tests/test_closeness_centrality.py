import networkx as nx
import nx_parallel as nxp
import math
import pytest


def test_betweenness_centrality_get_chunks():
    def get_chunk(nodes):
        num_chunks = nxp.get_n_jobs()
        nodes_ebc = {i: 0 for i in nodes}
        for i in ebc:
            nodes_ebc[i[0]] += ebc[i]
            nodes_ebc[i[1]] += ebc[i]

        sorted_nodes = sorted(nodes_ebc.items(), key=lambda x: x[1], reverse=True)

        chunks = [[] for _ in range(num_chunks)]
        chunk_sums = [0] * num_chunks

        for node, value in sorted_nodes:
            min_chunk_index = chunk_sums.index(min(chunk_sums))
            chunks[min_chunk_index].append(node)
            chunk_sums[min_chunk_index] += value

        return chunks

    G = nx.fast_gnp_random_graph(100, 0.1, directed=False)
    H = nxp.ParallelGraph(G)
    ebc = nx.edge_betweenness_centrality(G)
    par_bc_chunk = nxp.betweenness_centrality(H, get_chunks=get_chunk)  # smoke test
    par_bc = nxp.betweenness_centrality(H)

    for i in range(len(G.nodes)):
        assert math.isclose(par_bc[i], par_bc_chunk[i], abs_tol=1e-16)


def test_betweenness_centrality_directed_graph():
    """Test betweenness centrality on a directed graph."""
    G = nx.fast_gnp_random_graph(100, 0.1, directed=True)
    H = nxp.ParallelGraph(G)

    par_bc = nxp.betweenness_centrality(H)
    expected_bc = nx.betweenness_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_bc[node], expected_bc[node], abs_tol=1e-16)


def test_betweenness_centrality_weighted_graph():
    """Test betweenness centrality on a weighted graph."""
    G = nx.fast_gnp_random_graph(100, 0.1, directed=False)
    for u, v in G.edges:
        G[u][v]["weight"] = 1.0  # Assign uniform weights

    H = nxp.ParallelGraph(G)
    par_bc = nxp.betweenness_centrality(H, weight="weight")
    expected_bc = nx.betweenness_centrality(G, weight="weight")

    for node in G.nodes:
        assert math.isclose(par_bc[node], expected_bc[node], abs_tol=1e-16)


def test_betweenness_centrality_small_graph():
    """Test betweenness centrality on a small graph."""
    G = nx.path_graph(5)  # A simple path graph
    H = nxp.ParallelGraph(G)

    par_bc = nxp.betweenness_centrality(H)
    expected_bc = nx.betweenness_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_bc[node], expected_bc[node], abs_tol=1e-16)


def test_betweenness_centrality_empty_graph():
    """Test betweenness centrality on an empty graph."""
    G = nx.Graph()  # An empty graph
    H = nxp.ParallelGraph(G)

    # Check if the underlying graph is empty before calling the function
    if len(H.graph_object) == 0:  # Use the underlying graph's length
        assert (
            nxp.betweenness_centrality(H) == {}
        ), "Expected an empty dictionary for an empty graph"
    else:
        pytest.fail("Graph is not empty, but it should be.")


def test_betweenness_centrality_single_node():
    """Test betweenness centrality on a graph with a single node."""
    G = nx.Graph()
    G.add_node(1)
    H = nxp.ParallelGraph(G)

    par_bc = nxp.betweenness_centrality(H)
    expected_bc = nx.betweenness_centrality(G)

    assert par_bc == expected_bc  # Both should return {1: 0.0}


def test_betweenness_centrality_large_graph():
    """Test betweenness centrality on a large graph."""
    G = nx.fast_gnp_random_graph(1000, 0.01, directed=False)
    H = nxp.ParallelGraph(G)

    par_bc = nxp.betweenness_centrality(H)
    expected_bc = nx.betweenness_centrality(G)

    for node in G.nodes:
        assert math.isclose(
            par_bc[node], expected_bc[node], abs_tol=1e-6
        )  # Larger tolerance for large graphs


def test_betweenness_centrality_multigraph():
    """Test betweenness centrality on a multigraph."""
    G = nx.MultiGraph()
    G.add_edges_from([(1, 2), (1, 2), (2, 3), (3, 4)])
    H = nxp.ParallelGraph(G)

    par_bc = nxp.betweenness_centrality(H)
    expected_bc = nx.betweenness_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_bc[node], expected_bc[node], abs_tol=1e-16)


def test_closeness_centrality_default_chunks():
    """Test closeness centrality with default chunking."""
    G = nx.path_graph(5)  # A simple path graph
    H = nxp.ParallelGraph(G)

    par_cc = nxp.closeness_centrality(H, get_chunks="chunks")
    expected_cc = nx.closeness_centrality(G)

    for node in G.nodes:
        assert pytest.approx(par_cc[node], rel=1e-6) == expected_cc[node]


def test_closeness_centrality_custom_chunks():
    """Test closeness centrality with a custom chunking function."""

    def custom_chunking(nodes):
        # Example custom chunking: split nodes into two equal parts
        mid = len(nodes) // 2
        return [nodes[:mid], nodes[mid:]]

    G = nx.path_graph(5)  # A simple path graph
    H = nxp.ParallelGraph(G)

    par_cc = nxp.closeness_centrality(H, get_chunks=custom_chunking)
    expected_cc = nx.closeness_centrality(G)

    for node in G.nodes:
        assert pytest.approx(par_cc[node], rel=1e-6) == expected_cc[node]


def test_closeness_centrality_empty_graph():
    """Test closeness centrality on an empty graph."""
    G = nx.Graph()  # An empty graph
    H = nxp.ParallelGraph(G)

    assert (
        nxp.closeness_centrality(H, get_chunks="chunks") == {}
    ), "Expected an empty dictionary for an empty graph"


def test_closeness_centrality_single_node():
    """Test closeness centrality on a graph with a single node."""
    G = nx.Graph()
    G.add_node(1)
    H = nxp.ParallelGraph(G)

    par_cc = nxp.closeness_centrality(H, get_chunks="chunks")
    expected_cc = nx.closeness_centrality(G)

    assert par_cc == expected_cc  # Both should return {1: 0.0}


def test_closeness_centrality_large_graph():
    """Test closeness centrality on a large graph."""
    G = nx.fast_gnp_random_graph(1000, 0.01, directed=False)
    H = nxp.ParallelGraph(G)

    par_cc = nxp.closeness_centrality(H, get_chunks="chunks")
    expected_cc = nx.closeness_centrality(G)

    for node in G.nodes:
        assert pytest.approx(par_cc[node], rel=1e-6) == expected_cc[node]
