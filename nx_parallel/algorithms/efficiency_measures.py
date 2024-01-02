"""Provides functions for computing the efficiency of nodes and graphs."""
import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["local_efficiency"]


def local_efficiency(G, n_jobs=-1):
    """Returns the average local efficiency of the graph.

    The *efficiency* of a pair of nodes in a graph is the multiplicative
    inverse of the shortest path distance between the nodes. The *local
    efficiency* of a node in the graph is the average global efficiency of the
    subgraph induced by the neighbors of the node. The *average local
    efficiency* is the average of the local efficiencies of each node [1]_.

    Parameters
    ----------
    G : :class:`networkx.Graph`
        An undirected graph for which to compute the average local efficiency.

    n_jobs : int, optional (default=-1)
        The number of logical CPUs or cores you want to use. 
        For `n_jobs` less than 0, (`n_cpus + 1 + n_jobs`) are used.
        If an invalid value is given, then `n_jobs` is set to `n_cpus`.

    Returns
    -------
    float
        The average local efficiency of the graph.

    Notes
    -----
    Edge weights are ignored when computing the shortest path distances.

    References
    ----------
    .. [1] Latora, Vito, and Massimo Marchiori.
           "Efficient behavior of small-world networks."
           *Physical Review Letters* 87.19 (2001): 198701.
           <https://doi.org/10.1103/PhysRevLett.87.198701>
    """

    def _local_efficiency_node_subset(G, nodes):
        return sum(nx.global_efficiency(G.subgraph(G[v])) for v in nodes)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    num_in_chunk = max(len(G.nodes) // cpu_count, 1)
    node_chunks = list(nxp.chunks(G.nodes, num_in_chunk))

    efficiencies = Parallel(n_jobs=cpu_count)(
        delayed(_local_efficiency_node_subset)(G, chunk) for chunk in node_chunks
    )
    return sum(efficiencies) / len(G)
