from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = [
    "is_reachable",
    "tournament_is_strongly_connected",
]


def is_reachable(G, s, t):
    """The function parallelizes the calculation of two
    neighborhoods of vertices in `G` and checks closure conditions for each
    neighborhood subset in parallel.

    networkx.tournament.is_reachable : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_reachable.html#networkx.algorithms.tournament.is_reachable
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    G_adj = G._adj
    setG = set(G)

    cpu_count = nxp.cpu_count()

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
    num_in_chunk = max(len(G) // cpu_count, 1)

    # neighborhoods = [two_neighborhood_subset(G, chunk) for chunk in node_chunks]
    neighborhoods = Parallel(n_jobs=cpu_count)(
        delayed(two_nbrhood_subset)(G, chunk) for chunk in nxp.chunks(G, num_in_chunk)
    )

    # send chunk of neighborhoods to each process (checking closure conditions)
    nbrhoods = (nhood for nh_chunk in neighborhoods for nhood in nh_chunk)
    results = Parallel(n_jobs=cpu_count)(
        delayed(check_closure_subset)(ch) for ch in nxp.chunks(nbrhoods, num_in_chunk)
    )
    return all(results)


def tournament_is_strongly_connected(G):
    """The parallel computation is implemented by dividing the
    nodes into chunks and then checking whether each node is reachable from each
    other node in parallel.

    Note, this function uses the name `tournament_is_strongly_connected` while
    dispatching to the backend in=mplementation. So, `nxp.tournament.is_strongly_connected`
    will result in an error. Use `nxp.tournament_is_strongly_connected` instead.

    networkx.tournament.is_strongly_connected : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_strongly_connected.html#networkx.algorithms.tournament.is_strongly_connected
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    # Subset version of is_reachable
    def is_reachable_subset(G, chunk):
        return all(is_reachable(G, u, v) for v in chunk for u in G)

    cpu_count = nxp.cpu_count()
    num_in_chunk = max(len(G) // cpu_count, 1)
    node_chunks = nxp.chunks(G, num_in_chunk)

    results = Parallel(n_jobs=cpu_count)(
        delayed(is_reachable_subset)(G, chunk) for chunk in node_chunks
    )
    return all(results)
