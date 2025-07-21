from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp
from math import log
import itertools


__all__ = [
    "resource_allocation_index",
    "jaccard_coefficient",
    "adamic_adar_index",
    "preferential_attachment",
]


def _apply_prediction(G, func, ebunch=None, get_chunks="chunks"):
    """Applies the given function to each edge in the specified iterable
    of edges.
    """

    def _process_pair_chunk(pairs_chunk):
        return [(u, v, func(u, v)) for u, v in pairs_chunk]

    if ebunch is None:
        ebunch = nx.non_edges(G)
    else:
        for u, v in ebunch:
            if u not in G:
                raise nx.NodeNotFound(f"Node {u} not in G.")
            if v not in G:
                raise nx.NodeNotFound(f"Node {v} not in G.")

    ebunch = list(ebunch)
    if not ebunch:
        return iter([])

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        pairs_chunks = nxp.chunks(ebunch, n_jobs)
    else:
        pairs_chunks = get_chunks(ebunch)

    results = Parallel()(delayed(_process_pair_chunk)(chunk) for chunk in pairs_chunks)

    return sorted(list(itertools.chain.from_iterable(results)))


@nxp._configure_if_nx_active()
def resource_allocation_index(G, ebunch=None, get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the resource
    allocation index for all `pairs_chunks` is computed in parallel over
    `n_jobs` number of CPU cores.

    networkx.resource_allocation_index: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.resource_allocation_index.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    def predict(u, v):
        return sum(1 / G.degree(w) for w in nx.common_neighbors(G, u, v))

    if hasattr(G, "graph_object"):
        G = G.graph_object

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def jaccard_coefficient(G, ebunch=None, get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the jaccard
    coefficient for all `pairs_chunks` is computed in parallel over
    `n_jobs` number of CPU cores.

    networkx.jaccard_coefficient: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.jaccard_coefficient.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    def predict(u, v):
        union_size = len(set(G[u]) | set(G[v]))
        if union_size == 0:
            return 0
        return len(nx.common_neighbors(G, u, v)) / union_size

    if hasattr(G, "graph_object"):
        G = G.graph_object

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def adamic_adar_index(G, ebunch=None, get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the adamic
    adar index for all `pairs_chunks` is computed in parallel over
    `n_jobs` number of CPU cores.

    networkx.adamic_adar_index: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.adamic_adar_index.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    def predict(u, v):
        return sum(1 / log(G.degree(w)) for w in nx.common_neighbors(G, u, v))

    if hasattr(G, "graph_object"):
        G = G.graph_object

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def preferential_attachment(G, ebunch=None, get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the
    preferential attachment for all `pairs_chunks` is computed in
    parallel over `n_jobs` number of CPU cores.

    networkx.preferential_attachment: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.preferential_attachment.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    def predict(u, v):
        return G.degree(u) * G.degree(v)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    return _apply_prediction(G, predict, ebunch, get_chunks)
