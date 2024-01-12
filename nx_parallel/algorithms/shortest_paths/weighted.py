from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import single_source_bellman_ford_path
import nx_parallel as nxp

__all__ = ["all_pairs_bellman_ford_path"]


def all_pairs_bellman_ford_path(G, weight="weight"):
    """Parallel implementation of :func:`networkx.all_pairs_bellman_ford_path`
    Refer to it's for more details about the computation and parameter description.

    Returns shortest paths between all nodes in a weighted graph.

    Parallel Computation : The parallel computation is implemented by computing the 
    shortest paths for each node concurrently.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or function (default="weight")
        If string, then edge weights will be accessed like ``G.edges[u, v][weight]``.
        If function, the weight of an edge is the value returned by the function.

    Returns
    -------
    paths : iterator
        (source, dictionary) iterator with dictionary keyed by target and
        shortest path as the key value.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.Graph()
    >>> G.add_weighted_edges_from([(1, 0, 1), (1, 2, 1), (2, 0, 3)])
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

    cpu_count = nxp.cpu_count()

    nodes = G.nodes

    paths = Parallel(n_jobs=cpu_count, return_as="generator")(
        delayed(_calculate_shortest_paths_subset)(source) for source in nodes
    )
    return paths
