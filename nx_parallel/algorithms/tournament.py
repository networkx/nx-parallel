from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.simple_paths import is_simple_path as is_path
import networkx as nx

__all__ = [
    "is_reachable",
    "tournament_is_strongly_connected",
]


@nxp._configure_if_nx_active()
def is_reachable(G, s, t, get_chunks="chunks"):
    """The function parallelizes the calculation of two
    neighborhoods of vertices in `G` and checks closure conditions for each
    neighborhood subset in parallel.

    networkx.tournament.is_reachable : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_reachable.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """

    def two_neighborhood_close(G, chunk):
        tnc = []
        for v in chunk:
            S = {
                x
                for x in G
                if x == v or x in G[v] or any(is_path(G, [v, z, x]) for z in G)
            }
            tnc.append(not (is_closed(G, S) and s in S and t not in S))
        return all(tnc)

    def is_closed(G, nodes):
        return all(v in G[u] for u in set(G) - nodes for v in nodes)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        num_in_chunk = max(len(G) // n_jobs, 1)
        node_chunks = nxp.chunks(G, num_in_chunk)
    else:
        node_chunks = get_chunks(G)

    return all(
        Parallel()(delayed(two_neighborhood_close)(G, chunk) for chunk in node_chunks)
    )


@nxp._configure_if_nx_active()
def tournament_is_strongly_connected(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the
    nodes into chunks and then checking whether each node is reachable from each
    other node in parallel.

    Note, this function uses the name `tournament_is_strongly_connected` while
    dispatching to the backend implementation. So, `nxp.tournament.is_strongly_connected`
    will result in an error. Use `nxp.tournament_is_strongly_connected` instead.

    networkx.tournament.is_strongly_connected : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_strongly_connected.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    def is_reachable_subset(G, chunk):
        return all(nx.tournament.is_reachable(G, u, v) for v in chunk for u in G)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        num_in_chunk = max(min(len(G) // n_jobs, 10), 1)
        node_chunks = nxp.chunks(G, num_in_chunk)
    else:
        node_chunks = get_chunks(G)

    results = Parallel()(
        delayed(is_reachable_subset)(G, chunk) for chunk in node_chunks
    )
    return all(results)
