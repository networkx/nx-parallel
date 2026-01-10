from joblib import Parallel
from networkx.algorithms.bipartite.cluster import modes
import networkx as nx
import nx_parallel as nxp

__all__ = ["latapy_clustering"]


@nxp._configure_if_nx_active()
def latapy_clustering(G, nodes=None, mode="dot", get_chunks="chunks"):
    """In the parallel implementation we divide the nodes into chunks and compute
    the bipartite clustering coefficient for all `node_chunk` in parallel.

    networkx.bipartite.latapy_clustering : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.cluster.latapy_clustering.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` (or `nodes`) into `n_jobs` number of chunks.
    """

    def _process_chunk(chunks):
        ccs = {}
        for v in chunks:
            cc = 0.0
            nbrs2 = {u for nbr in G[v] for u in G[nbr]} - {v}
            for u in nbrs2:
                cc += cc_func(set(G[u]), set(G[v]))
            if cc > 0.0:  # len(nbrs2)>0
                cc /= len(nbrs2)
            ccs[v] = cc
        return ccs

    if hasattr(G, "graph_object"):
        G = G.graph_object

    try:
        cc_func = modes[mode]
    except KeyError as err:
        raise nx.NetworkXError(
            "Mode for bipartite clustering must be: dot, min or max"
        ) from err

    if nodes is None:
        nodes = G
    n_jobs = nxp.get_n_jobs()
    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)
    results = Parallel()((_process_chunk)(chunk) for chunk in node_chunks)

    clusterings = {}
    for result in results:
        for node, c in result.items():
            clusterings[node] += c

    return clusterings
