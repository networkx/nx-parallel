from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp

__all__ = ["closeness_centrality"]

@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
def closeness_centrality(G, u=None, distance=None, wf_improved=True):
    """
    Parallel implementation of networkx.closeness_centrality
    """
    if hasattr(G, "graph_object_"):
        G = G.graph_object_

    if u is None:
        nodes = list(G.nodes)
    else:
        nodes = list(nx.utils.nbunch_iter(u))

    # Helper: Calculate centrality for each node in the chunk manually
    def _process_chunk(chunk):
        chunk_results = {}
        for node in chunk:
            # NetworkX closeness only computes one node at a time if 'u' is set
            chunk_results[node] = nx.closeness_centrality(G, u=node, distance=distance, wf_improved=wf_improved)
        return chunk_results

    # 1. Split nodes into chunks
    n_jobs = nxp.get_n_jobs()
    node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)

    # 2. Process chunks in parallel
    results = Parallel(n_jobs=n_jobs)(
        delayed(_process_chunk)(chunk) for chunk in node_chunks
    )

    # 3. Combine results
    combined_results = {}
    for res in results:
        combined_results.update(res)

    return combined_results