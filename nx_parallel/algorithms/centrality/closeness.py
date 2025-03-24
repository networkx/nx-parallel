from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx

__all__ = ["closeness_centrality"]


@nxp._configure_if_nx_active()
def closeness_centrality(
    G, u=None, distance=None, wf_improved=True, get_chunks="chunks"
):
    """
    The parallel computation is implemented by dividing the nodes into chunks
    and computing closeness centrality for each chunk concurrently.

    Parameters
    ----------
    G : graph
      A NetworkX graph
    u : node, optional
      Return only the value for node u
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

    # Handle single node case directly
    if u is not None:
        nodes = [u]
    else:
        nodes = list(G.nodes)

    # For single node case, don't use parallelization
    if u is not None:
        result = _closeness_centrality_node_subset(G, nodes, distance, wf_improved)
        return result[u]

    n_jobs = nxp.get_n_jobs()

    # Validate get_chunks - the chunk parameter is only used for parallel execution
    if not (callable(get_chunks) or get_chunks == "chunks"):
        # Fallback to default chunking if get_chunks is invalid
        get_chunks = "chunks"

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        try:
            node_chunks = get_chunks(nodes)
        except:
            # Fallback if get_chunks fails
            node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)

    if not node_chunks:  # Handle empty chunks
        return {}

    cc_subs = Parallel()(
        delayed(_closeness_centrality_node_subset)(G, chunk, distance, wf_improved)
        for chunk in node_chunks
    )

    closeness_centrality_dict = {}
    for cc in cc_subs:
        closeness_centrality_dict.update(cc)

    return closeness_centrality_dict


def _closeness_centrality_node_subset(G, nodes, distance=None, wf_improved=True):
    """
    Compute closeness centrality for a subset of nodes.

    Implemented to match NetworkX's implementation exactly.
    """
    # Create a copy of the graph to avoid modifying the original
    # Handle directed graphs by reversing (matches NetworkX implementation)
    if G.is_directed():
        G = G.reverse()  # create a reversed graph view

    closeness_dict = {}

    for n in nodes:
        # Using the exact NetworkX path calculation logic
        if distance is not None:
            # Use Dijkstra for weighted graphs
            sp = nx.single_source_dijkstra_path_length(G, n, weight=distance)
        else:
            # Use BFS for unweighted graphs
            sp = nx.single_source_shortest_path_length(G, n)

        # Sum of shortest paths exactly as NetworkX does it
        totsp = sum(sp.values())
        len_G = len(G)
        _closeness_centrality = 0.0

        # Use the exact NetworkX formula and conditions
        if totsp > 0.0 and len_G > 1:
            _closeness_centrality = (len(sp) - 1.0) / totsp
            # Use the exact normalization formula from NetworkX
            if wf_improved:
                s = (len(sp) - 1.0) / (len_G - 1)
                _closeness_centrality *= s

        closeness_dict[n] = _closeness_centrality

    return closeness_dict
