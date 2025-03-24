from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx

__all__ = ["closeness_centrality"]


@nxp._configure_if_nx_active()
def closeness_centrality(
    G, distance=None, wf_improved=True, get_chunks="chunks"
):
    """
    The parallel computation is implemented by dividing the nodes into chunks
    and computing closeness centrality for each chunk concurrently.

    networkx.closeness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html

    Parameters
    ----------
    distance : string or function, optional
        The edge attribute to use as distance when computing shortest paths,
        or a user-defined distance function.
    wf_improved : bool, optional
        If True, use the improved formula for closeness centrality.
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

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    if not node_chunks:  # Handle empty chunks
        return {}

    cc_subs = Parallel()(
        delayed(_closeness_centrality_node_subset)(
            G, chunk, distance, wf_improved
        )
        for chunk in node_chunks
    )

    closeness_centrality_dict = cc_subs[0]
    for cc in cc_subs[1:]:
        closeness_centrality_dict.update(cc)

    return closeness_centrality_dict


def _closeness_centrality_node_subset(G, nodes, distance=None, wf_improved=True):
    """
    Compute closeness centrality for a subset of nodes.
    """
    closeness = {}
    for node in nodes:
        # Use NetworkX's built-in function for closeness centrality
        closeness[node] = nx.closeness_centrality(
            G, u=node, distance=distance, wf_improved=wf_improved
        )
    return closeness