from functools import partial
from joblib import Parallel, delayed
import networkx as nx
import networkx.parallel as nxp

__all__ = ["harmonic_centrality"]


@nxp._configure_if_nx_active()
def harmonic_centrality(
    G, nbunch=None, distance=None, sources=None, get_chunks="chunks"
):
    """Compute harmonic centrality in parallel.

    This implementation follows the approach used in betweenness centrality parallelization.

    Parameters
    ----------
    G : NetworkX graph
        A graph (directed or undirected).
    nbunch : container, optional (default: all nodes in G)
        Nodes for which harmonic centrality is calculated.
    sources : container, optional (default: all nodes in G)
        Nodes from which reciprocal distances are computed.
    distance : edge attribute key, optional (default: None)
        Use the specified edge attribute as the edge weight.
    get_chunks : str, function (default = "chunks")
        Function that takes a list of nodes as input and returns an iterable `node_chunks`.

    Returns
    -------
    dict
        Dictionary of nodes with harmonic centrality values.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nbunch = set(G.nbunch_iter(nbunch) if nbunch is not None else G.nodes)
    sources = set(G.nbunch_iter(sources) if sources is not None else G.nodes)

    centrality = {u: 0 for u in nbunch}

    transposed = False
    if len(nbunch) < len(sources):
        transposed = True
        nbunch, sources = sources, nbunch
        if nx.is_directed(G):
            G = nx.reverse(G, copy=False)

    # Get number of parallel jobs
    n_jobs = nxp.get_n_jobs()

    # Chunking nodes for parallel processing
    nodes = list(sources)
    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    def process_chunk(chunk):
        """Process a chunk of nodes and compute harmonic centrality."""
        local_centrality = {u: 0 for u in chunk}
        spl = partial(nx.shortest_path_length, G, weight=distance)

        for v in chunk:
            dist = spl(v)
            for u in nbunch.intersection(dist):
                d = dist[u]
                if d == 0:
                    continue
                local_centrality[v if transposed else u] += 1 / d

        return local_centrality

    # Run parallel processing on node chunks
    results = Parallel(n_jobs=n_jobs)(
        delayed(process_chunk)(chunk) for chunk in node_chunks
    )

    # Merge results
    for result in results:
        for node, value in result.items():
            centrality[node] += value

    return centrality
