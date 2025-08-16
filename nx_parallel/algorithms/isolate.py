import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["number_of_isolates"]


@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
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
        into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    isolates_list = list(nx.isolates(G))
    if get_chunks == "chunks":
        isolate_chunks = nxp.chunks(isolates_list, n_jobs)
    else:
        isolate_chunks = get_chunks(isolates_list)

    results = Parallel()(delayed(len)(chunk) for chunk in isolate_chunks)
    return sum(results)
