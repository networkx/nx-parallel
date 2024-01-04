from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import single_source_bellman_ford_path

import nx_parallel as nxp

__all__ = ["all_pairs_bellman_ford_path"]


def all_pairs_bellman_ford_path(G, weight="weight"):
    """Compute shortest paths between all nodes in a weighted graph.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or function (default="weight")
        If this is a string, then edge weights will be accessed via the
        edge attribute with this key (that is, the weight of the edge
        joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
        such edge attribute exists, the weight of the edge is assumed to
        be one.

        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly three
        positional arguments: the two endpoints of an edge and the
        dictionary of edge attributes for that edge. The function must
        return a number.

    Returns
    -------
    paths : iterator
        (source, dictionary) iterator with dictionary keyed by target and
        shortest path as the key value.

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.Graph()
    >>> G.add_weighted_edges_from([(1, 0, 1), (1, 2, 1), (2, 0, 3)])
    >>> path = dict(nx.all_pairs_bellman_ford_path(G))
    >>> path[0][2]
    [0, 1, 2]
    >>> parallel_path = dict(nx.all_pairs_bellman_ford_path(G, backend="parallel"))
    >>> parallel_path[0][2]
    [0, 1, 2]
    >>> import nx_parallel as nxp
    >>> parallel_path_ = dict(nx.all_pairs_bellman_ford_path(nxp.ParallelGraph(G)))
    >>> parallel_path_[0][2]
    [0, 1, 2]
    
    """

    def _calculate_shortest_paths_subset(source):
        return (source, single_source_bellman_ford_path(G, source, weight=weight))

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes

    total_cores = nxp.cpu_count()

    paths = Parallel(n_jobs=total_cores, return_as="generator")(
        delayed(_calculate_shortest_paths_subset)(source) for source in nodes
    )
    return paths
