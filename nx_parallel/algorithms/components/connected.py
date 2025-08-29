from networkx import connected_components
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["number_connected_components"]


@nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
def number_connected_components(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the list
    of connected components into chunks and then finding the length
    of each chunk in parallel and then adding all the lengths at the end.

    networkx.number_connected_components : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.number_connected_components.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of connected components as input and returns
        an iterable `component_chunks`. The default chunking is done by slicing the
        list of connected components into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    n_jobs = nxp.get_n_jobs()

    cc = list(connected_components(G))
    if get_chunks == "chunks":
        component_chunks = nxp.chunks(cc, n_jobs)
    else:
        component_chunks = get_chunks(cc)

    results = Parallel()(delayed(len)(chunk) for chunk in component_chunks)
    return sum(results)
