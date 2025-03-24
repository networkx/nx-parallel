from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx

__all__ = ["degree_centrality"]


@nxp._configure_if_nx_active()
def degree_centrality(G, get_chunks="chunks"):
    """
    Parallel computation of degree centrality. Divides nodes into chunks
    and computes degree centrality for each chunk concurrently.

    networkx.degree_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if len(G) == 0:  # Handle empty graph
        return {}

    nodes = list(G.nodes)
    n_jobs = nxp.get_n_jobs()

    # Create node subsets
    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    if not node_chunks:  # Handle empty chunks
        return {}

    # Compute degree centrality for each chunk in parallel
    dc_subs = Parallel()(
        delayed(_degree_centrality_node_subset)(G, chunk) for chunk in node_chunks
    )

    # Combine partial results
    degree_centrality_dict = dc_subs[0]
    for dc in dc_subs[1:]:
        degree_centrality_dict.update(dc)

    return degree_centrality_dict


def _degree_centrality_node_subset(G, nodes):
    part_dc = {}
    n = len(G)
    if n == 1:  # Handle single-node graph
        for node in nodes:
            part_dc[node] = 1.0
        return part_dc

    for node in nodes:
        part_dc[node] = G.degree[node] / (n - 1)
    return part_dc