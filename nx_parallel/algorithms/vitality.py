from functools import partial
import nx_parallel as nxp
from joblib import Parallel, delayed
import networkx as nx

__all__ = ["closeness_vitality"]


def closeness_vitality(G, node=None, weight=None, wiener_index=None):
    """The parallel computation is implemented only when the node
    is not specified. The closeness vitality for each node is computed concurrently.

    networkx.closeness_vitality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.vitality.closeness_vitality.html#closeness-vitality
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
