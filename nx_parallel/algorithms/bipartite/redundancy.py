from joblib import Parallel, delayed
from networkx.algorithms.bipartite.redundancy import _node_redundancy
import networkx as nx
import nx_parallel as nxp
from itertools import chain


__all__ = ["node_redundancy"]


@nxp._configure_if_nx_active()
def node_redundancy(G, nodes=None, get_chunks="chunks"):
    """In the parallel implementation we divide the nodes into chunks and compute
    the node redundancy coefficients for all `node_chunk` in parallel.

    networkx.bipartite.node_redundancy : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.redundancy.node_redundancy.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` (or `nodes`) into `n_jobs` number of chunks.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object
    if nodes is None:
        nodes = G
    if any(len(G[v]) < 2 for v in nodes):
        raise nx.NetworkXError(
            "Cannot compute redundancy coefficient for a node"
            " that has fewer than two neighbors."
        )
    n_jobs = nxp.get_n_jobs()
    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)
    node_redundancies = Parallel()(
        delayed(
            lambda G, node_chunk: [(v, _node_redundancy(G, v)) for v in node_chunk]
        )(G, node_chunk)
        for node_chunk in node_chunks
    )
    return dict(chain.from_iterable((node_redundancies)))
