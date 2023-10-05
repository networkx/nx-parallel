from joblib import Parallel, delayed

import nx_parallel as nxp

__all__ = [
    "is_reachable",
    "tournament_is_strongly_connected",
]


def is_reachable(G, s, t):
    """Decides whether there is a path from `s` to `t` in the tournament

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
    >>> import networkx as nx
    >>> G = nx.DiGraph([(1, 0), (1, 3), (1, 2), (2, 3), (2, 0), (3, 0)])
    >>> nx.tournament.is_tournament(G)
    True
    >>> nx.tournament.is_reachable(G, 1, 3, backend="parallel")
    True
    >>> import nx_parallel as nxp
    >>> nx.tournament.is_reachable(nxp.ParallelGraph(G), 3, 2)
    False
    >>> nx.tournament.is_reachable(G, 3, 2, backend="parallel")
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

    G_adj = G._adj
    setG = set(G)

    def two_nbrhood_subset(G, chunk):
        result = []
        for v in chunk:
            v_nbrs = G_adj[v].keys()
            result.append(v_nbrs | {x for nbr in v_nbrs for x in G_adj[nbr]})
        return result

    def is_closed(G, nodes):
        return all(v in G_adj[u] for u in setG - nodes for v in nodes)

    def check_closure_subset(chunk):
        return all(not (s in S and t not in S and is_closed(G, S)) for S in chunk)

    # send chunk of vertices to each process (calculating neighborhoods)
    num_in_chunk = max(len(G) // nxp.cpu_count(), 1)

    # neighborhoods = [two_neighborhood_subset(G, chunk) for chunk in node_chunks]
    neighborhoods = Parallel(n_jobs=-1)(
        delayed(two_nbrhood_subset)(G, chunk) for chunk in nxp.chunks(G, num_in_chunk)
    )

    # send chunk of neighborhoods to each process (checking closure conditions)
    nbrhoods = (nhood for nh_chunk in neighborhoods for nhood in nh_chunk)
    results = Parallel(n_jobs=-1, backend="loky")(
        delayed(check_closure_subset)(ch) for ch in nxp.chunks(nbrhoods, num_in_chunk)
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
    >>> import networkx as nx
    >>> G = nx.DiGraph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    >>> nx.tournament.is_tournament(G)
    True
    >>> import nx_parallel as nxp
    >>> nx.tournament.is_strongly_connected(nxp.ParallelGraph(G))
    False
    >>> nx.tournament.is_strongly_connected(G, backend="parallel")
    False
    >>> G.remove_edge(0, 3)
    >>> G.add_edge(3, 0)
    >>> nx.tournament.is_tournament(G)
    True
    >>> nx.tournament.is_strongly_connected(G, backend="parallel")
    True

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
        return all(is_reachable(G, u, v) for v in chunk for u in G)

    num_in_chunk = max(len(G) // nxp.cpu_count(), 1)
    results = Parallel(n_jobs=-1)(
        delayed(is_reachable_subset)(G, ch) for ch in nxp.chunks(G, num_in_chunk)
    )
    return all(results)
