from joblib import Parallel, delayed
from networkx.algorithms.centrality.betweenness import (
    _accumulate_basic,
    _accumulate_endpoints,
    _rescale,
    _single_source_dijkstra_path_basic,
    _single_source_shortest_path_basic,
)
from networkx.utils import py_random_state

import nx_parallel as nxp

__all__ = ["betweenness_centrality"]


@py_random_state(5)
def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    r"""Parallel Compute shortest-path betweenness centrality for nodes

    Betweenness centrality of a node $v$ is the sum of the
    fraction of all-pairs shortest paths that pass through $v$

    .. math::

       c_B(v) =\sum_{s,t \in V} \frac{\sigma(s, t|v)}{\sigma(s, t)}

    where $V$ is the set of nodes, $\sigma(s, t)$ is the number of
    shortest $(s, t)$-paths,  and $\sigma(s, t|v)$ is the number of
    those paths  passing through some  node $v$ other than $s, t$.
    If $s = t$, $\sigma(s, t) = 1$, and if $v \in {s, t}$,
    $\sigma(s, t|v) = 0$ [2]_.

    Parameters
    ----------
    G : graph
      A NetworkX graph.

    k : int, optional (default=None)
      If k is not None use k node samples to estimate betweenness.
      The value of k <= n where n is the number of nodes in the graph.
      Higher values give better approximation.

    normalized : bool, optional
      If True the betweenness values are normalized by `2/((n-1)(n-2))`
      for graphs, and `1/((n-1)(n-2))` for directed graphs where `n`
      is the number of nodes in G.

    weight : None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
      Weights are used to calculate weighted shortest paths, so they are
      interpreted as distances.

    endpoints : bool, optional
      If True include the endpoints in the shortest path counts.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
        Note that this is only used if k is not None.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with betweenness centrality as the value.

    Notes
    -----
    This algorithm is a parallelized version of betwenness centrality in NetworkX.
    Nodes are divided into chunks based on the number of available processors,
    and otherwise all calculations are similar.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if k is None:
        nodes = G.nodes
    else:
        nodes = seed.sample(list(G.nodes), k)

    total_cores = nxp.cpu_count()
    num_in_chunk = max(len(nodes) // total_cores, 1)
    node_chunks = nxp.chunks(nodes, num_in_chunk)

    bt_cs = Parallel(n_jobs=total_cores)(
        delayed(_betweenness_centrality_node_subset)(
            G,
            chunk,
            weight,
            endpoints,
        )
        for chunk in node_chunks
    )

    # Reducing partial solution
    bt_c = bt_cs[0]
    for bt in bt_cs[1:]:
        for n in bt:
            bt_c[n] += bt[n]

    betweenness = _rescale(
        bt_c,
        len(G),
        normalized=normalized,
        directed=G.is_directed(),
        k=k,
        endpoints=endpoints,
    )
    return betweenness


def _betweenness_centrality_node_subset(G, nodes, weight=None, endpoints=False):
    betweenness = dict.fromkeys(G, 0.0)
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        if endpoints:
            betweenness, delta = _accumulate_endpoints(betweenness, S, P, sigma, s)
        else:
            betweenness, delta = _accumulate_basic(betweenness, S, P, sigma, s)
    return betweenness
