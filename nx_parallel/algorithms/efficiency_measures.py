"""Provides functions for computing the efficiency of nodes and graphs."""

import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["global_efficiency", "local_efficiency"]


@nxp._configure_if_nx_active()
def global_efficiency(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the nodes into
    chunks and computing the inverse shortest-path lengths from each source node
    in each chunk concurrently, then summing the chunk totals and dividing by
    ``n * (n - 1)``.

    networkx.global_efficiency : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.efficiency_measures.global_efficiency.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """

    def _global_efficiency_node_subset(G, chunk):
        total = 0.0
        for source in chunk:
            lengths = nx.single_source_shortest_path_length(G, source)
            total += sum(1 / distance for distance in lengths.values() if distance > 0)
        return total

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if G.is_directed():
        raise nx.NetworkXNotImplemented("not implemented for directed type")

    n = len(G)
    denom = n * (n - 1)
    if denom == 0:
        return 0

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(G.nodes, n_jobs)
    else:
        node_chunks = get_chunks(G.nodes)

    efficiencies = Parallel()(
        delayed(_global_efficiency_node_subset)(G, chunk) for chunk in node_chunks
    )
    return sum(efficiencies) / denom


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
