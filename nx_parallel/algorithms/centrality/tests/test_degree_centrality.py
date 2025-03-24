import networkx as nx
import nx_parallel as nxp
import math


def test_degree_centrality_default_chunks():
    """Test degree centrality with default chunking."""
    G = nx.erdos_renyi_graph(100, 0.1, seed=42)  # Random graph with 100 nodes
    H = nxp.ParallelGraph(G)

    # Compute degree centrality using the parallel implementation
    par_dc = nxp.degree_centrality(H)

    # Compute degree centrality using NetworkX's built-in function
    expected_dc = nx.degree_centrality(G)

    # Compare the results
    for node in G.nodes:
        assert math.isclose(par_dc[node], expected_dc[node], abs_tol=1e-16)


def test_degree_centrality_custom_chunks():
    """Test degree centrality with custom chunking."""

    def get_chunk(nodes):
        num_chunks = nxp.get_n_jobs()
        chunks = [[] for _ in range(num_chunks)]
        for i, node in enumerate(nodes):
            chunks[i % num_chunks].append(node)
        return chunks

    G = nx.erdos_renyi_graph(100, 0.1, seed=42)
    H = nxp.ParallelGraph(G)

    # Compute degree centrality using custom chunking
    par_dc_chunk = nxp.degree_centrality(H, get_chunks=get_chunk)

    # Compute degree centrality using NetworkX's built-in function
    expected_dc = nx.degree_centrality(G)

    # Compare the results
    for node in G.nodes:
        assert math.isclose(par_dc_chunk[node], expected_dc[node], abs_tol=1e-16)


def test_degree_centrality_empty_graph():
    """Test degree centrality on an empty graph."""
    G = nx.Graph()  # Empty graph
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    assert par_dc == expected_dc  # Both should return an empty dictionary


def test_degree_centrality_single_node():
    """Test degree centrality on a graph with a single node."""
    G = nx.Graph()
    G.add_node(1)
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    assert par_dc == expected_dc  # Both should return {1: 0.0}


def test_degree_centrality_disconnected_graph():
    """Test degree centrality on a disconnected graph."""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])  # Add three disconnected nodes
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    assert par_dc == expected_dc  # Both should return {1: 0.0, 2: 0.0, 3: 0.0}


def test_degree_centrality_self_loops():
    """Test degree centrality on a graph with self-loops."""
    G = nx.Graph()
    G.add_edges_from([(1, 1), (2, 2), (2, 3)])  # Add self-loops and one normal edge
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_dc[node], expected_dc[node], abs_tol=1e-16)


def test_degree_centrality_directed_graph():
    """Test degree centrality on a directed graph."""
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])  # Create a directed cycle
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_dc[node], expected_dc[node], abs_tol=1e-16)


def test_degree_centrality_multigraph():
    """Test degree centrality on a multigraph."""
    G = nx.MultiGraph()
    G.add_edges_from([(1, 2), (1, 2), (2, 3)])  # Add multiple edges between nodes
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    for node in G.nodes:
        assert math.isclose(par_dc[node], expected_dc[node], abs_tol=1e-16)


def test_degree_centrality_large_graph():
    """Test degree centrality on a large graph."""
    G = nx.fast_gnp_random_graph(1000, 0.01, seed=42)
    H = nxp.ParallelGraph(G)

    # Compute degree centrality
    par_dc = nxp.degree_centrality(H)
    expected_dc = nx.degree_centrality(G)

    for node in G.nodes:
        assert math.isclose(
            par_dc[node], expected_dc[node], abs_tol=1e-6
        )  # Larger tolerance for large graphs
