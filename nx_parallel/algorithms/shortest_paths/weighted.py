from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import (
    single_source_bellman_ford_path
)

import nx_parallel as nxp

__all__ = ["all_pairs_bellman_ford_path"]


def all_pairs_bellman_ford_path(G, weight="weight"):
    """Compute shortest paths between all nodes in a weighted graph.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or function (default="weight")
        If this is a string, then edge weights will be accessed via the
        edge attribute with this key (that is, the weight of the edge
        joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
        such edge attribute exists, the weight of the edge is assumed to
        be one.

        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly three
        positional arguments: the two endpoints of an edge and the
        dictionary of edge attributes for that edge. The function must
        return a number.

    Returns
    -------
    all_paths : 
        dictionary keyed by source with value as another dictionary keyed 
        by target and shortest path as its key value.

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    nodes = G.nodes

    total_cores = nxp.cpu_count()
    
    num_in_chunk = max(len(nodes) // total_cores, 1)
    node_chunks = nxp.chunks(nodes, num_in_chunk)
    
    paths_list = Parallel(n_jobs=total_cores)(delayed(_calculate_shortest_paths_subset)(G, chunk, weight) for chunk in node_chunks)
    
    
    all_paths = {}
    for result in paths_list:
        for source, paths in result.items():
            all_paths[source]=paths
    return all_paths


# Helper function
def _calculate_shortest_paths_subset(G, chunk, weight):
    result = {}
    for source in chunk:
        paths = single_source_bellman_ford_path(G, source, weight=weight)
        result[source] = paths
    return result
