from functools import partial
from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp

__all__ = ["harmonic_centrality"]


@nxp._configure_if_nx_active()
def harmonic_centrality(
    G, u=None, distance=None, wf_improved=True, *, backend=None, **backend_kwargs
):
    """Compute harmonic centrality in parallel.

    Parameters
    ----------
    G : NetworkX graph
        A graph (directed or undirected).
    u : node or iterable, optional (default: all nodes in G)
        Compute harmonic centrality for the specified node(s).
    distance : edge attribute key, optional (default: None)
        Use the specified edge attribute as the edge weight.
    wf_improved : bool, optional (default: True)
        This parameter is included for API compatibility but not used in harmonic centrality.
    backend : str, optional (default: None)
        The parallel backend to use (`'loky'`, `'threading'`, etc.).
    **backend_kwargs : additional backend parameters

    Returns
    -------
    dict
        Dictionary of nodes with harmonic centrality values.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    u = set(G.nbunch_iter(u) if u is not None else G.nodes)
    sources = set(G.nodes)  # Always use all nodes as sources

    centrality = {v: 0 for v in u}

    transposed = False
    if len(u) < len(sources):
        transposed = True
        u, sources = sources, u
        if nx.is_directed(G):
            G = nx.reverse(G, copy=False)

    # Get number of parallel jobs
    n_jobs = nxp.get_n_jobs()

    # Chunking nodes for parallel processing
    nodes = list(sources)
    node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)

    def process_chunk(chunk):
        """Process a chunk of nodes and compute harmonic centrality."""
        local_centrality = {v: 0 for v in chunk}
        spl = partial(nx.shortest_path_length, G, weight=distance)

        for v in chunk:
            dist = spl(v)
            for node in u.intersection(dist):
                d = dist[node]
                if d == 0:
                    continue
                local_centrality[v if transposed else node] += 1 / d

        return local_centrality

    # Run parallel processing on node chunks
    results = Parallel(n_jobs=n_jobs, backend=backend, **backend_kwargs)(
        delayed(process_chunk)(chunk) for chunk in node_chunks
    )

    # Merge results
    for result in results:
        for node, value in result.items():
            centrality[node] += value

    return centrality
