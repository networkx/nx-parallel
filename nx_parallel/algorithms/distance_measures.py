"""Graph diameter"""

import networkx as nx
import nx_parallel as nxp
from joblib import Parallel, delayed

__all__ = ["diameter"]


@nxp._configure_if_nx_active()
def diameter(G, e=None, usebounds=False, weight=None, get_chunks="chunks"):
    """This alternative to the more general `diameter` function is faster and
    allows for an approximation tolerance, though the default is to find the
    exact zero-tolerance result. The function uses the Iterative Fringe Upper
    Bound (IFUB) algorithm [1]_ with parallel computation of BFSes for fringe
    vertices.

    networkx.diameter : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html#networkx.algorithms.distance_measures.diameter

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.

    Notes
    -----
    The IFUB algorithm first selects an approximate "central" node using
    the 4-sweep heuristic. The 4-sweep method starts from a random node,
    finds its farthest node, then repeats this process four times to
    approximate a central node. A BFS tree is then rooted at this node,
    and eccentricities are computed layer-wise in parallel. If the max eccentricity
    from a layer exceeds twice the layer index, the algorithm terminates
    and returns the diameter; otherwise, it proceeds further. IFUB is
    observed to compute diameters efficiently for real-world graphs [1]_.

    References
    ----------
    .. [1] Crescenzi, P., Grossi, R., Lanzi, L., & Marino, A.
        "On computing the diameter of real-world undirected graphs"
        Theoretical Computer Science 426 (2012): 34-52.
        https://doi.org/10.1016/j.tcs.2012.09.018
    """
    G = G.graph_object if isinstance(G, nxp.ParallelGraph) else G

    if not nx.is_connected(G):
        raise nx.NetworkXError("Cannot compute metric because graph is not connected.")

    start_node = max(G.nodes(), key=G.degree)
    lower_bound = 0

    # First BFS from start_node
    layers = list(nx.bfs_layers(G, start_node))
    max_level_node = layers[-1][0] if layers[-1] else None

    # Second BFS from max_level_node
    layers = list(nx.bfs_layers(G, max_level_node))
    max_level = len(layers) - 1
    max_level_node = layers[-1][0] if layers[-1] else None
    lower_bound = max(lower_bound, max_level)

    # Find a mid-level node
    mid_level = max_level // 2
    mid_level_node = (
        layers[mid_level][0] if mid_level < len(layers) and layers[mid_level] else None
    )

    # Third BFS from mid_level_node
    layers = list(nx.bfs_layers(G, mid_level_node))
    max_level_node = layers[-1][0] if layers[-1] else None

    # Fourth BFS from max_level_node
    layers = list(nx.bfs_layers(G, max_level_node))
    max_level = len(layers) - 1
    max_level_node = layers[-1][0] if layers[-1] else None
    lower_bound = max(lower_bound, max_level)

    # Find a mid-level node from the last BFS
    mid_level = max_level // 2
    mid_level_node = (
        layers[mid_level][0] if mid_level < len(layers) and layers[mid_level] else None
    )

    error_tolerance = 0
    root = mid_level_node
    layers = list(nx.bfs_layers(G, root))
    max_level = len(layers) - 1
    upper_bound = 2 * max_level
    lower_bound = max(lower_bound, max_level)
    cur_level = max_level
    level_vertices = dict(enumerate(layers))

    n_jobs = nxp.get_n_jobs()

    while upper_bound - lower_bound > error_tolerance:
        fringe_vertices = level_vertices.get(cur_level, [])

        if not fringe_vertices:
            cur_level -= 1
            continue

        # Parallelize the eccentricity calculation for fringe vertices
        if get_chunks == "chunks":
            vertex_chunks = nxp.create_iterables(G, "node", n_jobs, fringe_vertices)
        else:
            vertex_chunks = get_chunks(fringe_vertices)

        # Calculate eccentricity for each chunk in parallel
        chunk_eccentricities = Parallel()(
            delayed(_calculate_eccentricities_for_nodes)(G, chunk)
            for chunk in vertex_chunks
        )

        # Find the maximum eccentricity across all chunks
        cur_max_ecc = (
            max(max(eccs.values()) for eccs in chunk_eccentricities)
            if chunk_eccentricities
            else 0
        )

        if max(lower_bound, cur_max_ecc) > 2 * (cur_level - 1):
            return max(lower_bound, cur_max_ecc)
        else:
            lower_bound = max(lower_bound, cur_max_ecc)
            upper_bound = 2 * (cur_level - 1)

        cur_level -= 1

    return lower_bound


def _calculate_eccentricities_for_nodes(G, nodes):
    """Calculate eccentricities for a subset of nodes."""
    eccentricities = {-1: 0}
    for node in nodes:
        layers = list(nx.bfs_layers(G, node))
        eccentricities[node] = len(layers) - 1
    return eccentricities
