"""
Closeness centrality measures.
"""

from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["closeness_centrality"]


def closeness_centrality(
    G, u=None, distance=None, wf_improved=True, blocking_factor=None
):
    """The parallel implementation of closeness centrality, that use parallel tiled floy warshall to find the
    geodesic distance of the node

    networkx.closeness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html

    Parameters
    ----------
    blocking_factor : number
        The number used for divinding the adjacency matrix in sub-matrix.
        The default blocking factor is get by finding the optimal value
        for the core available
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if G.is_directed():
        G = G.reverse()  # create a reversed graph view

    A = nxp.floyd_warshall_numpy(G, blocking_factor=blocking_factor)

    len_G = len(G)

    closeness_dict = Parallel(n_jobs=-1)(
        delayed(_closeness_measure(n, wf_improved, len_G))(A) for n in A
    )

    if u is not None:
        return closeness_dict[u]
    return closeness_dict


def _closeness_measure(n, wf_improved, len_G):
    """calculate the closeness centrality measure of one node using the row of edges i

    Parameters
    ----------
    n : 1D numpy.ndarray
        the array of distance from every other node

    Returns
    -------
    k : numebr
        the closeness value for the selected node
    """
    totsp = sum(n)
    closeness_value = 0.0
    if totsp > 0.0 and len_G > 1:
        closeness_value = (len(n) - 1.0) / totsp
        # normalize to number of nodes-1 in connected part
        if wf_improved:
            s = (len(n) - 1.0) / (len_G - 1)
            closeness_value *= s

    return closeness_value
