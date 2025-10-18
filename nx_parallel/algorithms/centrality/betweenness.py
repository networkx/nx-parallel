from joblib import Parallel, delayed
from networkx.algorithms.centrality.betweenness import (
    _accumulate_basic,
    _accumulate_endpoints,
    _single_source_dijkstra_path_basic,
    _single_source_shortest_path_basic,
    _rescale,
    _add_edge_keys,
    _accumulate_edges,
)
from networkx.utils import py_random_state
import nx_parallel as nxp

__all__ = ["betweenness_centrality", "edge_betweenness_centrality"]


@nxp._configure_if_nx_active()
@py_random_state(5)
def betweenness_centrality(
    G,
    k=None,
    normalized=True,
    weight=None,
    endpoints=False,
    seed=None,
    get_chunks="chunks",
):
    """The parallel computation is implemented by dividing the nodes into chunks and
    computing betweenness centrality for each chunk concurrently.

    networkx.betweenness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if not G:
        return {}

    if k == len(G):
        k = None

    if k is None:
        nodes = G.nodes
    else:
        nodes = seed.sample(list(G.nodes), k)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    bt_cs = Parallel()(
        delayed(_betweenness_centrality_node_subset)(G, chunk, weight, endpoints)
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
        endpoints=endpoints,
        sampled_nodes=None if k is None else nodes,
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


@nxp._configure_if_nx_active()
@py_random_state(4)
def edge_betweenness_centrality(
    G, k=None, normalized=True, weight=None, seed=None, get_chunks="chunks"
):
    """The parallel computation is implemented by dividing the nodes into chunks and
        computing edge betweenness centrality for each chunk concurrently.

    networkx.edge_betweenness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.edge_betweenness_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if not G:
        return {}

    if k is None:
        nodes = G.nodes
    else:
        nodes = seed.sample(list(G.nodes), k)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    bt_cs = Parallel()(
        delayed(_edge_betweenness_centrality_node_subset)(G, chunk, weight)
        for chunk in node_chunks
    )

    # Reducing partial solution
    bt_c = bt_cs[0]
    for bt in bt_cs[1:]:
        for e in bt:
            bt_c[e] += bt[e]

    for n in G:  # remove nodes to only return edges
        del bt_c[n]

    betweenness = _rescale(
        bt_c,
        len(G),
        normalized=normalized,
        directed=G.is_directed(),
        sampled_nodes=None if k is None else nodes,
    )

    if G.is_multigraph():
        betweenness = _add_edge_keys(G, betweenness, weight=weight)

    return betweenness


def _edge_betweenness_centrality_node_subset(G, nodes, weight=None):
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # b[e]=0 for e in G.edges()
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        betweenness = _accumulate_edges(betweenness, S, P, sigma, s)
    return betweenness
