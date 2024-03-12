import networkx as nx
import nx_parallel as nxp
import time
import math


def test_betweenness_centrality_get_chunks():
    def get_chunk(nodes, num_chunks):
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

    G = nx.bipartite.random_graph(400, 700, 0.8, seed=5, directed=False)
    H = nxp.ParallelGraph(G)
    ebc = nx.edge_betweenness_centrality(G)
    t1 = time.time()
    par_bc_chunk = nxp.betweenness_centrality(H, get_chunks=get_chunk)  # smoke test
    t2 = time.time()
    par_bc = nxp.betweenness_centrality(H)
    t3 = time.time()
    for i in range(len(G.nodes)):
        assert math.isclose(par_bc[i], par_bc_chunk[i], abs_tol=1e-16)
    with_chunk = t2 - t1
    without_chunk = t3 - t2
    assert with_chunk < without_chunk
    # get_chunk is faster than default(for big graphs)
