import networkx as nx
import nx_parallel as nxp
import math


def test_harmonic_centrality_get_chunks():
    def get_chunk(nodes):
        num_chunks = nxp.get_n_jobs()
        node_hc = {i: 0 for i in nodes}

        for node in nodes:
            node_hc[node] = sum(
                1 / d
                for _, d in nx.single_source_shortest_path_length(G, node).items()
                if d > 0
            )

        sorted_nodes = sorted(node_hc.items(), key=lambda x: x[1], reverse=True)

        chunks = [[] for _ in range(num_chunks)]
        chunk_sums = [0] * num_chunks

        for node, value in sorted_nodes:
            min_chunk_index = chunk_sums.index(min(chunk_sums))
            chunks[min_chunk_index].append(node)
            chunk_sums[min_chunk_index] += value

        return chunks

    # Create a random graph
    G = nx.fast_gnp_random_graph(100, 0.1, directed=False)
    H = nxp.ParallelGraph(G)

    # Compute harmonic centrality with and without chunking
    par_hc_chunk = nxp.harmonic_centrality(H, get_chunks=get_chunk)
    par_hc = nxp.harmonic_centrality(H)

    # Validate results
    for node in G.nodes:
        assert math.isclose(par_hc[node], par_hc_chunk[node], abs_tol=1e-16)
