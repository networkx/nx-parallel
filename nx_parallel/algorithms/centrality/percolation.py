from joblib import Parallel, delayed
import networkx as nx
from networkx.algorithms.centrality.betweenness import (
    _single_source_dijkstra_path_basic,
    _single_source_shortest_path_basic,
)
from networkx.algorithms.centrality.percolation import _accumulate_percolation

import nx_parallel as nxp


__all__ = ["percolation_centrality"]


@nxp._configure_if_nx_active()
def percolation_centrality(
    G,
    attribute="percolation",
    states=None,
    weight=None,
    get_chunks="chunks",
):
    """The parallel computation is implemented by dividing the source nodes into
    chunks and computing their percolation centrality contributions concurrently.

    networkx.percolation_centrality :
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.percolation_centrality.html

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

    nodes = G.nodes

    if states is None:
        states = nx.get_node_attributes(G, attribute, default=1)

    p_sigma_x_t = sum(states.values())

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    partial_percolation = Parallel()(
        delayed(_percolation_centrality_node_subset)(
            G,
            chunk,
            states,
            p_sigma_x_t,
            weight,
        )
        for chunk in node_chunks
    )

    percolation = partial_percolation[0]
    for partial in partial_percolation[1:]:
        for node in partial:
            percolation[node] += partial[node]

    n = len(G)
    for node in percolation:
        percolation[node] *= 1 / (n - 2)

    return percolation


def _percolation_centrality_node_subset(
    G,
    nodes,
    states,
    p_sigma_x_t,
    weight=None,
):
    percolation = dict.fromkeys(G, 0.0)

    for s in nodes:
        if weight is None:
            S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
        else:
            S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)

        percolation = _accumulate_percolation(
            percolation,
            S,
            P,
            sigma,
            s,
            states,
            p_sigma_x_t,
        )

    return percolation
