import networkx as nx
import nx_parallel as nxp
import pytest

def test_eccentricity():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    assert nx.eccentricity(G) == nxp.eccentricity(H)
    assert nx.eccentricity(G, v=0) == nxp.eccentricity(H, v=0)
    assert nx.eccentricity(G, v=[0, 1]) == nxp.eccentricity(H, v=[0, 1])

def test_eccentricity_directed():
    G = nx.DiGraph([(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)]) # Strongly connected
    H = nxp.ParallelGraph(G)
    assert nx.eccentricity(G) == nxp.eccentricity(H)

def test_eccentricity_not_connected():
    G = nx.Graph([(0, 1), (2, 3)])
    H = nxp.ParallelGraph(G)
    with pytest.raises(nx.NetworkXError):
        nxp.eccentricity(H)

def test_eccentricity_sp():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    sp = dict(nx.all_pairs_shortest_path_length(G))
    assert nx.eccentricity(G, sp=sp) == nxp.eccentricity(H, sp=sp)

def test_diameter():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    assert nx.diameter(G) == nxp.diameter(H)

def test_radius():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    assert nx.radius(G) == nxp.radius(H)

def test_center():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    assert nx.center(G) == nxp.center(H)

def test_periphery():
    G = nx.path_graph(5)
    H = nxp.ParallelGraph(G)
    assert nx.periphery(G) == nxp.periphery(H)
