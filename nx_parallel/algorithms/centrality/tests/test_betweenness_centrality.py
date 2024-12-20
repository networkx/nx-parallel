import networkx as nx
import nx_parallel as nxp
import math


def test_edge_betweenness_centrality_get_chunks():
    def get_chunk(edges):
        num_chunks = nxp.get_n_jobs()

        edges = list(edges)

        # Split edges into chunks without relying on precomputed centrality
        chunk_size = max(1, len(edges) // num_chunks)
        chunks = [edges[i : i + chunk_size] for i in range(0, len(edges), chunk_size)]

        print(f"Chunks distribution: {chunks}")

        return chunks

    G = nx.fast_gnp_random_graph(100, 0.1, directed=False)
    H = nxp.ParallelGraph(G)

    ebc = nx.edge_betweenness_centrality(G, normalized=True)

    print(f"NetworkX Edge Betweenness Centrality: {ebc}")

    backend = nxp.BackendInterface()

    # Smoke test for edge_betweenness_centrality with custom get_chunks
    par_bc_chunk = backend.edge_betweenness_centrality(
        H.graph_object,
        get_chunks=get_chunk,
    )

    print(f"Parallel Computed Edge Betweenness Centrality: {par_bc_chunk}")

    # Compare with standard edge betweenness centrality
    standard_bc = nx.edge_betweenness_centrality(G, normalized=True)

    for edge in standard_bc:
        assert math.isclose(
            par_bc_chunk[edge], standard_bc[edge], abs_tol=1e-6
        ), f"Edge {edge} mismatch: {par_bc_chunk[edge]} vs {standard_bc[edge]}"
