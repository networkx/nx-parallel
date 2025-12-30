import networkx as nx
import nx_parallel as nxp


def test_harmonic_centrality():
    print("\nTesting Harmonic Centrality...")
    # Create a random graph
    G = nx.gnp_random_graph(50, 0.5, seed=42)

    # 1. Run Standard NetworkX
    H_nx = nx.harmonic_centrality(G)

    # 2. Run Your Parallel Version
    H_par = nxp.harmonic_centrality(G)

    # 3. Compare results
    assert H_nx == H_par
    print("SUCCESS: Parallel result matches NetworkX exactly!")
