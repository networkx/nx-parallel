import networkx as nx
import nx_parallel as nxp


def test_voterank_get_chunks():
    def get_chunk(nodes):
        num_chunks = nxp.get_n_jobs()
        sorted_nodes = sorted(nodes, key=lambda n: G.degree(n), reverse=True)

        chunks = [[] for _ in range(num_chunks)]
        chunk_sums = [0] * num_chunks

        for node in sorted_nodes:
            min_chunk_index = chunk_sums.index(min(chunk_sums))
            chunks[min_chunk_index].append(node)
            chunk_sums[min_chunk_index] += G.degree(node)

        return chunks

    # Generate a random graph
    G = nx.fast_gnp_random_graph(100, 0.1, directed=False)
    H = nxp.ParallelGraph(G)

    # Compute VoteRank with and without chunking
    par_vr_chunk = nxp.voterank(H, get_chunks=get_chunk)
    par_vr = nxp.voterank(H)

    # Ensure both methods produce the same influential nodes
    assert par_vr_chunk == par_vr
