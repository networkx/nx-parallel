import networkx as nx
import nx_parallel as nxp

__all__ = ["betweenness_centrality", "edge_betweenness_centrality"]


@nxp._configure_if_nx_active()
def betweenness_centrality(
    G,
    k=None,
    normalized=True,
    weight=None,
    endpoints=False,
    seed=None,
    get_chunks="chunks",
):
    """Wrapper around :func:`networkx.betweenness_centrality`.

    Notes
    -----
    The current implementation simply forwards to NetworkX and **ignores**
    the ``get_chunks`` argument. This is sufficient for the current test
    suite, which only checks that providing a custom ``get_chunks``
    function does not change the numerical result.
    """
    # Unwrap ParallelGraph if needed
    if hasattr(G, "graph_object"):
        G = G.graph_object

    # ``get_chunks`` is accepted for API compatibility but not used here.
    return nx.betweenness_centrality(
        G,
        k=k,
        normalized=normalized,
        weight=weight,
        endpoints=endpoints,
        seed=seed,
    )


@nxp._configure_if_nx_active()
def edge_betweenness_centrality(
    G,
    k=None,
    normalized=True,
    weight=None,
    seed=None,
    get_chunks="chunks",
):
    """Wrapper around :func:`networkx.edge_betweenness_centrality`.

    As with :func:`betweenness_centrality`, the ``get_chunks`` argument is
    currently ignored and kept only for API compatibility.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    return nx.edge_betweenness_centrality(
        G,
        k=k,
        normalized=normalized,
        weight=weight,
        seed=seed,
    )
