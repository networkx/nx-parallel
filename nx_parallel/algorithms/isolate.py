import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["number_of_isolates"]


def number_of_isolates(G):
    """Parallel implementation of :func:`networkx.algorithms.isolates.number_of_isolates`
    
    Returns the number of isolates in `G`.

    Refer to :func:`networkx.algorithms.isolates.number_of_isolates` for more details.

    Parallel Computation
    ---------------------
    The parallel computation is implemented by dividing the list of isolated nodes
    into chunks and then finding the length of each chunk in parallel
    and then adding all the lengths at the end.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    Examples
    --------
    >>> import networkx as nx
    >>> import nx_parallel as nxp
    >>> G = nx.Graph()
    >>> G.add_edge(1, 2)
    >>> G.add_node(3)
    >>> list(nx.isolates(G))
    [3]
    >>> nxp.number_of_isolates(G)
    1
    >>> nx.number_of_isolates(G, backend="parallel")
    1
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
