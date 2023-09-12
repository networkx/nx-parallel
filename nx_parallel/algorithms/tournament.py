from joblib import Parallel, cpu_count, delayed
from networkx.algorithms.simple_paths import is_simple_path as is_path

from nx_parallel.algorithms.utils.chunk import chunks

__all__ = [
    "is_reachable",
    "tournament_is_strongly_connected",
]


def is_reachable(G, s, t):
    """Decides whether there is a path from `s` to `t` in the
    tournament.

    This function is more theoretically efficient than the reachability
    checks than the shortest path algorithms in
    :mod:`networkx.algorithms.shortest_paths`.

    The given graph **must** be a tournament, otherwise this function's
    behavior is undefined.

    Parameters
    ----------
    G : NetworkX graph
        A directed graph representing a tournament.

    s : node
        A node in the graph.

    t : node
        A node in the graph.

    Returns
    -------
    bool
        Whether there is a path from `s` to `t` in `G`.

    Examples
    --------
    >>> from networkx.algorithms import tournament
    >>> G = nx.DiGraph([(1, 0), (1, 3), (1, 2), (2, 3), (2, 0), (3, 0)])
    >>> tournament.is_reachable(G, 1, 3)
    True
    >>> tournament.is_reachable(G, 3, 2)
    False

    Notes
    -----
    Although this function is more theoretically efficient than the
    generic shortest path functions, a speedup requires the use of
    parallelism. Though it may in the future, the current implementation
    does not use parallelism, thus you may not see much of a speedup.

    This algorithm comes from [1].

    References
    ----------
    .. [1] Tantau, Till.
           "A note on the complexity of the reachability problem for
           tournaments."
           *Electronic Colloquium on Computational Complexity*. 2001.
           <http://eccc.hpi-web.de/report/2001/092/>
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    def two_neighborhood_subset(G, chunk):
        reList = set()
        for v in chunk:
            reList.update(
                {
                    x
                    for x in G
                    if x == v or x in G[v] or any(is_path(G, [v, z, x]) for z in G)
                }
            )
        return reList

    def is_closed(G, nodes):
        return all(v in G[u] for u in set(G) - nodes for v in nodes)

    def check_closure_subset(chunk):
        return not any((s in S and t not in S and is_closed(G, S)) for S in chunk)

    # send chunk of vertices to each process (calculating neighborhoods)
    num_chunks = max(len(G) // cpu_count(), 1)
    node_chunks = list(chunks(G.nodes, num_chunks))

    # neighborhoods = [two_neighborhood_subset(G, chunk) for chunk in node_chunks]
    neighborhoods = Parallel(n_jobs=-1)(
        delayed(two_neighborhood_subset)(G, chunk) for chunk in node_chunks
    )

    # send chunk of neighborhoods to each process (checking closure conditions)
    neighborhood_chunks = list(chunks(neighborhoods, num_chunks))
    #    results = [check_closure_subset(chunk) for chunk in neighborhood_chunks]
    results = Parallel(n_jobs=-1, backend="loky")(
        delayed(check_closure_subset)(chunk) for chunk in neighborhood_chunks
    )
    return all(results)


def tournament_is_strongly_connected(G):
    """Decides whether the given tournament is strongly connected.

    This function is more theoretically efficient than the
    :func:`~networkx.algorithms.components.is_strongly_connected`
    function.

    The given graph **must** be a tournament, otherwise this function's
    behavior is undefined.

    Parameters
    ----------
    G : NetworkX graph
        A directed graph representing a tournament.

    Returns
    -------
    bool
        Whether the tournament is strongly connected.

    Examples
    --------
    >>> from networkx.algorithms import tournament
    >>> G = nx.DiGraph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 0)])
    >>> tournament.is_strongly_connected(G)
    True
    >>> G.remove_edge(1, 3)
    >>> tournament.is_strongly_connected(G)
    False

    Notes
    -----
    Although this function is more theoretically efficient than the
    generic strong connectivity function, a speedup requires the use of
    parallelism. Though it may in the future, the current implementation
    does not use parallelism, thus you may not see much of a speedup.

    This algorithm comes from [1].

    References
    ----------
    .. [1] Tantau, Till.
           "A note on the complexity of the reachability problem for
           tournaments."
           *Electronic Colloquium on Computational Complexity*. 2001.
           <http://eccc.hpi-web.de/report/2001/092/>

    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    # Subset version of is_reachable

    def is_reachable_subset(G, chunk):
        re = set()
        for v in chunk:
            re.update(is_reachable(G, u, v) for u in G)
        return all(re)

    num_chunks = max(len(G) // cpu_count(), 1)
    node_chunks = list(chunks(G.nodes, num_chunks))
    #    results = [is_reachable_subset(G, chunk) for chunk in node_chunks]
    results = Parallel(n_jobs=-1)(
        delayed(is_reachable_subset)(G, chunk) for chunk in node_chunks
    )
    return all(results)
