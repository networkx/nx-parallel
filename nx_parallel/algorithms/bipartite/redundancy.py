from joblib import Parallel, delayed
from networkx.algorithms.bipartite.redundancy import _node_redundancy
import networkx as nx
import nx_parallel as nxp
from itertools import chain


__all__ = ["node_redundancy"]


def node_redundancy(G, nodes=None, get_chunks="chunks"):
    """In the parallel implementation we divide the nodes into chunks and compute
    the node redundancy coefficients for all `node_chunk` in parallel.

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in an iterable of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `G.nodes` (or `nodes`) into `n` chunks, where `n` is the number of CPU cores.

    networkx.bipartite.node_redundancy : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.redundancy.node_redundancy.html"""

    if hasattr(G, "graph_object"):
        G = G.graph_object
    if nodes is None:
        nodes = G
    if any(len(G[v]) < 2 for v in nodes):
        raise nx.NetworkXError(
            "Cannot compute redundancy coefficient for a node"
            " that has fewer than two neighbors."
        )
    total_cores = nxp.cpu_count()
    if get_chunks == "chunks":
        num_in_chunk = max(len(nodes) // total_cores, 1)
        node_chunks = nxp.chunks(nodes, num_in_chunk)
    else:
        node_chunks = get_chunks(nodes)
    node_redundancies = Parallel(n_jobs=total_cores)(
        delayed(
            lambda G, node_chunk: [(v, _node_redundancy(G, v)) for v in node_chunk]
        )(G, node_chunk)
        for node_chunk in node_chunks
    )
    return dict(chain.from_iterable((node_redundancies)))
