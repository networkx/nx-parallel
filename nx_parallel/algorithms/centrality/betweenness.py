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

    Parameters
    ------------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n` chunks, where `n` is the number of CPU cores.

    networkx.betweenness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if k is None:
        nodes = G.nodes
    else:
        nodes = seed.sample(list(G.nodes), k)

    total_cores = nxp.cpu_count()

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", total_cores, nodes)
    else:
        node_chunks = get_chunks(nodes)

    bt_cs = Parallel(n_jobs=total_cores)(
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
