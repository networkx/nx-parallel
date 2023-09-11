"""Provides functions for computing the efficiency of nodes and graphs."""
from joblib import Parallel, cpu_count, delayed
from nx_parallel.algorithms.utils.chunk import chunks
from nx_parallel.classes.graph import (
    ParallelGraph,
    ParallelDiGraph,
    ParallelMultiDiGraph,
    ParallelMultiGraph,
)
import networkx as nx
from networkx.utils import not_implemented_for

__all__ = ["local_efficiency"]

"""Helper to interface between graph types"""


def _convert(G):
    if isinstance(G, ParallelMultiDiGraph):
        return ParallelMultiDiGraph.to_networkx(G)
    if isinstance(G, ParallelMultiGraph):
        return ParallelMultiGraph.to_networkx(G)
    if isinstance(G, ParallelDiGraph):
        return ParallelDiGraph.to_networkx(G)
    if isinstance(G, ParallelGraph):
        return ParallelGraph.to_networkx(G)


@not_implemented_for("directed")
def efficiency(G, u, v):
    return nx.efficiency(_convert(G), u, v)


@not_implemented_for("directed")
def global_efficiency(G):
    return nx.global_efficiency(_convert(G))


@not_implemented_for("directed")
def local_efficiency(G):
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

    Returns
    -------
    float
        The average local efficiency of the graph.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
    >>> nx.local_efficiency(G)
    0.9166666666666667

    Notes
    -----
    Edge weights are ignored when computing the shortest path distances.

    See also
    --------
    global_efficiency

    References
    ----------
    .. [1] Latora, Vito, and Massimo Marchiori.
           "Efficient behavior of small-world networks."
           *Physical Review Letters* 87.19 (2001): 198701.
           <https://doi.org/10.1103/PhysRevLett.87.198701>
    """
    total_cores = cpu_count()
    num_chunks = max(len(G.nodes) // total_cores, 1)
    node_chunks = list(chunks(G.nodes, num_chunks))
    efficiencies = Parallel(n_jobs=total_cores)(
        delayed(local_efficiency_node_subset)(G, chunk) for chunk in node_chunks
    )
    return sum(efficiencies) / len(G)


def local_efficiency_node_subset(G, nodes):
    return sum(global_efficiency(G.subgraph(G[v])) for v in nodes)
