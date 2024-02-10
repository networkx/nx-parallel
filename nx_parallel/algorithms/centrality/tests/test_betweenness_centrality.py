import networkx as nx
import nx_parallel as nxp


def test_betweenness_centrality_get_chunks():
    def get_chunk(nodes, num_chunks):
        ebc = nx.edge_betweenness_centrality(G)
        nodes_ebc = {i: 0 for i in G.nodes}
        for i in ebc:
            nodes_ebc[i[0]] += ebc[i]
            nodes_ebc[i[1]] += ebc[i]

        sorted_ebc = sorted(nodes_ebc.items(), key=lambda x: x[1])

        chunks_with_avg = [[] for _ in range(num_chunks)]
        chunk_sums = [0] * num_chunks

        # Assign values to chunks based on balancing the sums
        for key, value in sorted_ebc:
            # Find the chunk with the smallest sum and add the value to it
            min_chunk = min(enumerate(chunk_sums), key=lambda x: x[1])[0]
            chunks_with_avg[min_chunk].append((key, value))
            chunk_sums[min_chunk] += value

        chunks = [[j[0] for j in i] for i in chunks_with_avg]

        return chunks

    G = nx.fast_gnp_random_graph(50, 0.5, directed=False)
    par_bc = nxp.betweenness_centrality(G, get_chunks=get_chunk)  # smoke test
    bc = nx.betweenness_centrality(G)
    for i in range(20):
        assert round(par_bc[i], 15) == round(bc[i], 15)
