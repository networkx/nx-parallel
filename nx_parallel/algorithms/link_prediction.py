from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp
from math import log
import itertools
from networkx.algorithms.link_prediction import _community


__all__ = [
    "resource_allocation_index",
    "jaccard_coefficient",
    "adamic_adar_index",
    "preferential_attachment",
    "common_neighbor_centrality",
    "cn_soundarajan_hopcroft",
    "ra_index_soundarajan_hopcroft",
    "within_inter_cluster",
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
        return []

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        pairs_chunks = nxp.chunks(ebunch, n_jobs)
    else:
        pairs_chunks = get_chunks(ebunch)

    results = Parallel()(delayed(_process_pair_chunk)(chunk) for chunk in pairs_chunks)

    return itertools.chain.from_iterable(results)


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


@nxp._configure_if_nx_active()
def common_neighbor_centrality(G, ebunch=None, alpha=0.8, get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the
    common neighbor centrality for all `pairs_chunks` is computed
    in parallel over `n_jobs` number of CPU cores.

    networkx.common_neighbor_centrality: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.common_neighbor_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if alpha == 1:

        def predict(u, v):
            if u == v:
                raise nx.NetworkXAlgorithmError("Self loops are not supported")

            return len(nx.common_neighbors(G, u, v))

    else:
        spl = dict(nx.shortest_path_length(G))
        inf = float("inf")

        def predict(u, v):
            if u == v:
                raise nx.NetworkXAlgorithmError("Self loops are not supported")
            path_len = spl[u].get(v, inf)

            n_nbrs = len(nx.common_neighbors(G, u, v))
            return alpha * n_nbrs + (1 - alpha) * len(G) / path_len

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def cn_soundarajan_hopcroft(G, ebunch=None, community="community", get_chunks="chunks"):
    """The edge pairs are chunked into `pairs_chunks` and then the
    number of common neighbors for all `pairs_chunks` is computed
    in parallel, using community information, over `n_jobs` number
    of CPU cores.

    networkx.cn_soundarajan_hopcroft: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.cn_soundarajan_hopcroft.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    def predict(u, v):
        Cu = _community(G, u, community)
        Cv = _community(G, v, community)
        cnbors = nx.common_neighbors(G, u, v)
        neighbors = (
            sum(_community(G, w, community) == Cu for w in cnbors) if Cu == Cv else 0
        )
        return len(cnbors) + neighbors

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def ra_index_soundarajan_hopcroft(
    G, ebunch=None, community="community", get_chunks="chunks"
):
    """The edge pairs are chunked into `pairs_chunks` and then the resource
    allocation index for all `pairs_chunks` is computed in parallel, using the
    community information, over `n_jobs` number of CPU cores.

    networkx.ra_index_soundarajan_hopcroft: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.ra_index_soundarajan_hopcroft.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    def predict(u, v):
        Cu = _community(G, u, community)
        Cv = _community(G, v, community)
        if Cu != Cv:
            return 0
        cnbors = nx.common_neighbors(G, u, v)
        return sum(1 / G.degree(w) for w in cnbors if _community(G, w, community) == Cu)

    return _apply_prediction(G, predict, ebunch, get_chunks)


@nxp._configure_if_nx_active()
def within_inter_cluster(
    G, ebunch=None, delta=0.001, community="community", get_chunks="chunks"
):
    """The edge pairs are chunked into `pairs_chunks` and then the ratio
    of within- and inter-cluster common neighbors is computed, for all
    `pairs_chunks` in parallel over `n_jobs` number of CPU cores.

    networkx.within_inter_cluster: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.within_inter_cluster.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the edges (or ebunch) as input and
        returns an iterable `pairs_chunks`. The default chunking is done by slicing
        `ebunch` into `n_jobs` number of chunks.
    """
    if delta <= 0:
        raise nx.NetworkXAlgorithmError("Delta must be greater than zero")

    if hasattr(G, "graph_object"):
        G = G.graph_object

    def predict(u, v):
        Cu = _community(G, u, community)
        Cv = _community(G, v, community)
        if Cu != Cv:
            return 0
        cnbors = nx.common_neighbors(G, u, v)
        within = {w for w in cnbors if _community(G, w, community) == Cu}
        inter = cnbors - within
        return len(within) / (len(inter) + delta)

    return _apply_prediction(G, predict, ebunch, get_chunks)
