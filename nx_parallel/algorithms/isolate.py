import networkx as nx
from joblib import Parallel, delayed

import nx_parallel as nxp

__all__ = ["number_of_isolates"]


def number_of_isolates(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the list
    of isolated nodes into chunks and then finding the length of each chunk in parallel
    and then adding all the lengths at the end.

    networkx.number_of_isolates : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isolate.number_of_isolates.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the isolated nodes as input and returns an
        iterable `isolate_chunks`. The default chunking is done by slicing the `isolates`
        into `n` chunks, where `n` is the total number of CPU cores available.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    isolates_list = list(nx.isolates(G))
    if get_chunks == "chunks":
        num_in_chunk = max(len(isolates_list) // cpu_count, 1)
        isolate_chunks = nxp.chunks(isolates_list, num_in_chunk)
    else:
        isolate_chunks = get_chunks(isolates_list)

    results = Parallel(n_jobs=cpu_count)(
        delayed(len)(chunk) for chunk in isolate_chunks
    )
    return sum(results)
