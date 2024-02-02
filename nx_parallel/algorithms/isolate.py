import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["number_of_isolates_chunk", "number_of_isolates_no_chunk"]


def number_of_isolates_chunk(G):
    """The parallel computation is implemented by dividing the list
    of isolated nodes into chunks and then finding the length of each chunk in parallel
    and then adding all the lengths at the end.

    networkx.number_of_isolates : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isolate.number_of_isolates.html#number-of-isolates
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    isolates_list = list(nx.isolates(G))
    num_in_chunk = max(len(isolates_list) // cpu_count, 1)
    isolate_chunks = nxp.chunks(isolates_list, num_in_chunk)
    results = Parallel(n_jobs=cpu_count)(
        delayed(len)(chunk) for chunk in isolate_chunks
    )
    return sum(results)

def number_of_isolates_no_chunk(G):
    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    results = Parallel(n_jobs=cpu_count)(delayed(lambda v: 1)(v) for v in nx.isolates(G))
    
    return sum(results)
