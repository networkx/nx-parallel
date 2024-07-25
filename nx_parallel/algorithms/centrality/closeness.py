__all__ = ["closeness_centrality"]


def closeness_centrality(
    G, u=None, distance=None, wf_improved=True, blocking_factor=None
):
    """The parallel implementation first divide the nodes into chunks and

    networkx.closeness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html

    Parameters
    ----------
    blocking_factor : number
        The number used for divinding the adjacency matrix in sub-matrix.
        The default blocking factor is get by finding the optimal value
        for the core available
    """
