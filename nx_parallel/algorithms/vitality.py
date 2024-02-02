from functools import partial
import nx_parallel as nxp
from joblib import Parallel, delayed
import networkx as nx

__all__ = ["closeness_vitality_no_chunk", "closeness_vitality_chunk"]


def closeness_vitality_no_chunk(G, node=None, weight=None, wiener_index=None):
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

    vitality = partial(closeness_vitality_no_chunk, G, weight=weight, wiener_index=wiener_index)
    result = Parallel(n_jobs=cpu_count)(
        delayed(lambda v: (v, vitality(v)))(v) for v in G
    )
    return dict(result)


def closeness_vitality_chunk(G, node=None, weight=None, wiener_index=None):
    """The parallel computation is implemented only when the node
    is not specified. The closeness vitality for each node is computed concurrently.

    networkx.closeness_vitality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.vitality.closeness_vitality.html#closeness-vitality
    """

    def closeness_vitality_chunk_subset(chunk):
        return {v: vitality(v) for v in chunk}
    
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if wiener_index is None:
        wiener_index = nx.wiener_index(G, weight=weight)

    if node is not None:
        after = nx.wiener_index(G.subgraph(set(G) - {node}), weight=weight)
        return wiener_index - after

    cpu_count = nxp.cpu_count()
    num_in_chunk = max(len(G) // cpu_count, 1)
    node_chunks = nxp.chunks(G.nodes, num_in_chunk)


    vitality = partial(closeness_vitality_chunk, G, weight=weight, wiener_index=wiener_index)
    
    result = Parallel(n_jobs=cpu_count)(
        delayed(closeness_vitality_chunk_subset)(chunk) for chunk in node_chunks
    )
    return {k: v for d in result for k, v in d.items()}

