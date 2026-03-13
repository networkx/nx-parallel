from itertools import combinations, chain
from collections import Counter
from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx
from networkx.algorithms.cluster import (
    _directed_weighted_triangles_and_degree_iter,
    _directed_triangles_and_degree_iter,
    _weighted_triangles_and_degree_iter,
    _triangles_and_degree_iter,
)

__all__ = [
    "square_clustering",
    "triangles",
    "clustering",
    "average_clustering",
]


@nxp._configure_if_nx_active()
def square_clustering(G, nodes=None, get_chunks="chunks"):
    """The nodes are chunked into `node_chunks` and then the square clustering
    coefficient for all `node_chunks` are computed in parallel over `n_jobs` number
    of CPU cores.

    networkx.square_clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.square_clustering.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _compute_clustering_chunk(node_iter_chunk):
        result_chunk = []
        for v in node_iter_chunk:
            clustering = 0
            potential = 0
            v_nbrs = G_nbrs_as_sets[v]
            for u, w in combinations(v_nbrs, 2):
                u_nbrs = G_nbrs_as_sets[u]
                w_nbrs = G_nbrs_as_sets[w]
                squares = len((u_nbrs & w_nbrs) - {v})
                clustering += squares
                degm = squares + 1
                if w in u_nbrs:
                    degm += 1
                potential += (len(u_nbrs) - degm) + (len(w_nbrs) - degm) + squares
            if potential > 0:
                clustering /= potential
            result_chunk += [(v, clustering)]
        return result_chunk

    if hasattr(G, "graph_object"):
        G = G.graph_object

    # ignore self-loops as per networkx 3.5
    G_nbrs_as_sets = {node: set(G[node]) - {node} for node in G}

    node_iter = list(G.nbunch_iter(nodes))

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_iter_chunks = nxp.chunks(node_iter, n_jobs)
    else:
        node_iter_chunks = get_chunks(node_iter)

    result = Parallel()(
        delayed(_compute_clustering_chunk)(node_iter_chunk)
        for node_iter_chunk in node_iter_chunks
    )
    clustering = dict(chain.from_iterable(result))

    if nodes in G:
        return clustering[nodes]
    return clustering


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_nodes_none)
def triangles(G, nodes=None, get_chunks="chunks"):
    """The nodes are chunked into `node_chunks` and for all `node_chunks`
    the number of triangles that include a node as one vertex is computed
    in parallel over `n_jobs` number of CPU cores.

    networkx.triangles : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.triangles.html#networkx.algorithms.cluster.triangles.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _compute_triangles_chunk(node_iter_chunk, later_nbrs):
        triangle_counts = Counter()
        for node1 in node_iter_chunk:
            neighbors = later_nbrs[node1]
            for node2 in neighbors:
                third_nodes = neighbors & later_nbrs[node2]
                m = len(third_nodes)
                triangle_counts[node1] += m
                triangle_counts[node2] += m
                triangle_counts.update(third_nodes)
        return triangle_counts

    if hasattr(G, "graph_object"):
        G = G.graph_object

    # Use parallel version only if nodes is None (i.e., all nodes requested)
    if nodes is not None:
        if nodes in G:
            return next(_triangles_and_degree_iter(G, nodes))[2] // 2
        return {v: t // 2 for v, d, t, _ in _triangles_and_degree_iter(G, nodes)}

    # Use parallel version for all nodes in G
    nodes = list(G)

    later_nbrs = {}
    for node, neighbors in G.adjacency():
        later_nbrs[node] = {n for n in neighbors if n not in later_nbrs and n != node}

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_iter_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_iter_chunks = get_chunks(nodes)

    results = Parallel()(
        delayed(_compute_triangles_chunk)(node_iter_chunk, later_nbrs)
        for node_iter_chunk in node_iter_chunks
    )

    triangle_counts = Counter(dict.fromkeys(G, 0))
    for result in results:
        triangle_counts.update(result)
    return triangle_counts


@nxp._configure_if_nx_active()
def clustering(G, nodes=None, weight=None, get_chunks="chunks"):
    """The nodes are chunked into `node_chunks` and then the clustering
    coefficient for all `node_chunks` is computed in parallel over `n_jobs`
    number of CPU cores.

    networkx.clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.clustering.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _compute_chunk(chunk):
        if G.is_directed():
            if weight is not None:
                td_iter = _directed_weighted_triangles_and_degree_iter(G, chunk, weight)
                clusterc = {
                    v: 0 if t == 0 else t / ((dt * (dt - 1) - 2 * db) * 2)
                    for v, dt, db, t in td_iter
                }
            else:
                td_iter = _directed_triangles_and_degree_iter(G, chunk)
                clusterc = {
                    v: 0 if t == 0 else t / ((dt * (dt - 1) - 2 * db) * 2)
                    for v, dt, db, t in td_iter
                }
        else:
            # The formula 2*T/(d*(d-1)) from docs is t/(d*(d-1)) here b/c t==2*T
            if weight is not None:
                td_iter = _weighted_triangles_and_degree_iter(G, chunk, weight)
                clusterc = {
                    v: 0 if t == 0 else t / (d * (d - 1)) for v, d, t in td_iter
                }
            else:
                td_iter = _triangles_and_degree_iter(G, chunk)
                clusterc = {
                    v: 0 if t == 0 else t / (d * (d - 1)) for v, d, t, _ in td_iter
                }
        return clusterc

    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    nodes_to_chunk = list(G.nbunch_iter(nodes))

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes_to_chunk, n_jobs)
    else:
        node_chunks = get_chunks(nodes_to_chunk)

    results = Parallel()(delayed(_compute_chunk)(chunk) for chunk in node_chunks)

    clusterc = {}
    for result in results:
        clusterc.update(result)

    if nodes in G:
        return clusterc[nodes]
    return clusterc


@nxp._configure_if_nx_active()
def average_clustering(
    G, nodes=None, weight=None, count_zeros=True, get_chunks="chunks"
):
    """The nodes are chunked into `node_chunks` and then the average clustering
    coefficient for all `node_chunks` is computed in parallel over `n_jobs`
    number of CPU cores.

    networkx.average_clustering: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.average_clustering.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _compute_chunk(chunk):
        return nx.clustering(G, chunk, weight=weight)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    if nodes is None:
        nodes = list(G)

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)

    results = Parallel()(delayed(_compute_chunk)(chunk) for chunk in node_chunks)

    clustering = {}
    for result in results:
        clustering.update(result)

    c = clustering.values()

    if not count_zeros:
        c = [v for v in c if abs(v) > 0]

    return sum(c) / len(c)
