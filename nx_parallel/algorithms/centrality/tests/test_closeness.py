import networkx as nx
import nx_parallel as nxp


def test_closeness_centrality():
    print("\nTesting Closeness Centrality...")
    G = nx.gnp_random_graph(50, 0.5, seed=42)

    # 1. Standard NetworkX
    H_nx = nx.closeness_centrality(G)

    # 2. Parallel Version
    H_par = nxp.closeness_centrality(G)

    # 3. Compare
    assert H_nx == H_par
    print("SUCCESS: Parallel Closeness matches NetworkX exactly!")
