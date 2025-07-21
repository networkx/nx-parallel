from itertools import combinations, chain
from collections import Counter
from joblib import Parallel, delayed
from networkx.algorithms.cluster import _triangles_and_degree_iter
import nx_parallel as nxp

__all__ = [
    "square_clustering",
    "triangles",
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


@nxp._configure_if_nx_active()
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

    if nodes is not None:
        if nodes in G:
            return next(_triangles_and_degree_iter(G, nodes))[2] // 2
        return {v: t // 2 for v, d, t, _ in _triangles_and_degree_iter(G, nodes)}
    else:
        nodes = list(G.nodes())

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
