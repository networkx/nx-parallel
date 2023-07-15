from joblib import Parallel, delayed, cpu_count
from nx_parallel.classes.graph import ParallelGraph, ParallelDiGraph,ParallelMultiDiGraph, ParallelMultiGraph
from nx_parallel.algorithms.utils.chunk import chunks
import networkx as nx
from networkx.utils import py_random_state
from networkx.algorithms.centrality.betweenness import (
    _rescale, 
    _single_source_shortest_path_basic, 
    _single_source_dijkstra_path_basic, 
    _accumulate_endpoints, 
    _accumulate_basic
)
__all__ = ["betweenness_centrality"]

"""Helper to interface between graph types"""
def _convert(G):
    if isinstance(G, ParallelMultiDiGraph):
        I = ParallelMultiDiGraph.to_networkx(G)
    if isinstance(G, ParallelMultiGraph):
        I = ParallelMultiGraph.to_networkx(G)
    if isinstance(G, ParallelDiGraph):
        I = ParallelDiGraph.to_networkx(G)
    if isinstance(G, ParallelGraph):
        I = ParallelGraph.to_networkx(G)
    return I

@py_random_state(5)
def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    r"""Compute the shortest-path betweenness centrality for nodes. Parallel implementation.

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
    This algorithm is a parallelized version of betwenness centrality in NetworkX. Nodes are divided into
    chunks based on the number of available processors, and otherwise all calculations are similar

    References
    ----------
    .. [1] Ulrik Brandes:
       A Faster Algorithm for Betweenness Centrality.
       Journal of Mathematical Sociology 25(2):163-177, 2001.
       https://doi.org/10.1080/0022250X.2001.9990249
    .. [2] Linton C. Freeman:
       A set of measures of centrality based on betweenness.
       Sociometry 40: 35–41, 1977
       https://doi.org/10.2307/3033543
    .. [3] Linton C. Freeman:
       A set of measures of centrality based on betweenness.
       Sociometry 40: 35–41, 1977
       https://doi.org/10.2307/3033543
    .. [4] NetworkX Development Team:
       Parallel Betweenness Centrality. NetworkX documentation.
       Available at: https://networkx.org/documentation/stable/auto_examples/algorithms/plot_parallel_betweenness.html
       Accessed on June 26, 2023.
    """    
    I = _convert(G)
    if k is None:
        nodes = G.nodes
    else:
        nodes = seed.sample(list(G.nodes), k)
    total_cores = cpu_count()
    num_chunks = max(len(nodes) // total_cores, 1)
    node_chunks = list(chunks(nodes, num_chunks))
    bt_cs = Parallel(n_jobs=total_cores)(
        delayed(betweenness_centrality_node_subset)(
            I,
            chunk,
            weight,
            endpoints,
        )
        for chunk in node_chunks
    )

    #Reducing partial solution
    bt_c = bt_cs[0]
    for bt in bt_cs[1:]:
        for n in bt:
            bt_c[n] += bt[n]

    betweenness = _rescale(
        bt_c,
        len(G),
        normalized=normalized,
        directed=I.is_directed(),
        k=k,
        endpoints=endpoints,
    )
    return betweenness



def betweenness_centrality_node_subset(G, nodes, weight=None, endpoints=False):
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







