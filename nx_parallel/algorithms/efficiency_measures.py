"""Provides functions for computing the efficiency of nodes and graphs."""

import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["local_efficiency"]


@nxp._configure_if_nx_active()
def local_efficiency(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the
    nodes into chunks and then computing and adding global efficiencies of all node
    in all chunks, in parallel, and then adding all these sums and dividing by the
    total number of nodes at the end.

    networkx.local_efficiency : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.efficiency_measures.local_efficiency.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """

    def _local_efficiency_node_subset(G, chunk):
        return sum(nx.global_efficiency(G.subgraph(G[v])) for v in chunk)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = list(nxp.chunks(G.nodes, n_jobs))
    else:
        node_chunks = get_chunks(G.nodes)

    efficiencies = Parallel()(
        delayed(_local_efficiency_node_subset)(G, chunk) for chunk in node_chunks
    )
    return sum(efficiencies) / len(G)
