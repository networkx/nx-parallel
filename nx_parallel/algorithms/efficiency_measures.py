"""Provides functions for computing the efficiency of nodes and graphs."""
import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["local_efficiency"]


def local_efficiency(G):
    """
    Parallel implementation of :func:`networkx.algorithms.efficiency.local_efficiency`

    Returns the average local efficiency of the graph.
    The *average local efficiency* is the average of the local efficiencies of 
    each node. The *efficiency* of a pair of nodes in a graph is the multiplicative
    inverse of the shortest path distance between the nodes.

    Refer :func:`networkx.algorithms.efficiency.local_efficiency` for more details.

    Parallel Computation
    ---------------------
    The parallel computation is implemented by dividing the nodes into chunks and
    then computing and adding global efficiencies of all node in all chunks,
    in parallel, and then adding all these sums and dividing by the total number
    of nodes at the end.

    Parameters
    ----------
    G : :class:`networkx.Graph`
        An undirected graph

    Returns
    -------
    float
        The average local efficiency of the graph.

    Examples
    --------
    >>> import networkx as nx
    >>> import nx_parallel as nxp
    >>> G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
    >>> nx.local_efficiency(G)
    0.9166666666666667
    >>> nxp.local_efficiency(G)
    0.9166666666666667
    >>> nx.local_efficiency(G, backend="parallel")
    0.9166666666666667
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
