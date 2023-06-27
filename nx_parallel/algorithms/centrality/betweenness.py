from joblib import Parallel, delayed
import multiprocessing
import itertools
from networkx import betweenness_centrality_subset

__all__ = ["betweenness_centrality"]


def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
    """Compute the shortest-path betweenness centrality for nodes. Parallel implementation.

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
    # TODO: Work on passing all tests for betweenness_centrality
    total_cores = multiprocessing.cpu_count()
    num_nodes = len(G)
    num_chunks = max(num_nodes // total_cores, 1)
    node_chunks = list(_chunks(G.nodes(), num_chunks))
    bt_sc = Parallel(n_jobs=total_cores, backend="loky")(
        delayed(betweenness_centrality_subset)(
            G,
            nodes,
            list(G),
            normalized,
            weight,
        )
        for nodes in node_chunks
    )

    #Reducing partial solution
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]

    return bt_c

# helpers for betweenness centrality

def _chunks(l, n): # divide vertices into chunks of specified size
    l_c = iter(l)
    while True:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


