from functools import partial
import nx_parallel as nxp
from joblib import Parallel, delayed
import networkx as nx

__all__ = ["closeness_vitality"]


def closeness_vitality(G, node=None, weight=None, wiener_index=None):
    """
    Parallel implementation of :func:`networkx.algorithms.vitality.closeness_vitality`
    
    Rreturns the closeness vitality for nodes in `G`. 
    *Closeness vitality* of a node is the change in the sum of 
    distances between all node pairs when excluding that node.

    The parallel computation is implemented only when the node is not specified.
    The closeness vitality for each node is computed concurrently.

    Refer to :func:`networkx.algorithms.vitality.closeness_vitality` for more details.

    Parameters
    ----------
    G : NetworkX graph
        A strongly-connected graph.

    weight : string
        The name of the edge attribute used as weight.

    node : object
        If specified, only the closeness vitality for this node will be
        returned. Otherwise, a dictionary mapping each node to its
        closeness vitality will be returned.

    Other parameters
    ----------------
    wiener_index : number
        If you have already computed the Wiener index of the graph
        `G`, you can provide that value here.

    Returns
    -------
    dictionary or float
        Returns a dictionary with nodes as keys and closeness vitality as values,
        based on the `node` parameter.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if wiener_index is None:
        wiener_index = nx.wiener_index(G, weight=weight)

    if node is not None:
        after = nx.wiener_index(G.subgraph(set(G) - {node}), weight=weight)
        return wiener_index - after

    cpu_count = nxp.cpu_count()

    vitality = partial(closeness_vitality, G, weight=weight, wiener_index=wiener_index)
    result = Parallel(n_jobs=cpu_count)(
        delayed(lambda v: (v, vitality(v)))(v) for v in G
    )
    return dict(result)
