from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp

__all__ = ["eccentricity", "diameter", "radius", "center", "periphery"]


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
def eccentricity(G, v=None, sp=None, weight=None, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the nodes into chunks and
    computing eccentricity for each chunk concurrently.

    networkx.eccentricity : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.eccentricity.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    # Fallback to sequential for single node or if shortest paths are provided
    if sp is not None or (v is not None and v in G):
        return nx.eccentricity(G, v, sp, weight)

    nodes = list(G.nbunch_iter(v))
    if not nodes:
        return {}

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    results = Parallel()(
        delayed(_eccentricity_chunk)(G, chunk, weight) for chunk in node_chunks
    )

    ecc = {}
    for result in results:
        ecc.update(result)

    return ecc


def _eccentricity_chunk(G, nodes, weight):
    order = G.order()
    e = {}
    for n in nodes:
        length = nx.shortest_path_length(G, source=n, weight=weight)
        if len(length) != order:
            if G.is_directed():
                msg = (
                    "Found infinite path length because the digraph is not"
                    " strongly connected"
                )
            else:
                msg = "Found infinite path length because the graph is not connected"
            raise nx.NetworkXError(msg)
        e[n] = max(length.values())
    return e


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
def diameter(G, e=None, useIP=False, get_chunks="chunks"):
    """The parallel computation is implemented by using the parallel eccentricity
    implementation.

    networkx.diameter : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if e is None:
        e = eccentricity(G, get_chunks=get_chunks)
    return max(e.values())


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
def radius(G, e=None, useIP=False, get_chunks="chunks"):
    """The parallel computation is implemented by using the parallel eccentricity
    implementation.

    networkx.radius : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.radius.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if e is None:
        e = eccentricity(G, get_chunks=get_chunks)
    return min(e.values())


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
def center(G, e=None, useIP=False, get_chunks="chunks"):
    """The parallel computation is implemented by using the parallel eccentricity
    implementation.

    networkx.center : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.center.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if e is None:
        e = eccentricity(G, get_chunks=get_chunks)
    r = min(e.values())
    p = [v for v, ecc in e.items() if ecc == r]
    return p


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
def periphery(G, e=None, useIP=False, get_chunks="chunks"):
    """The parallel computation is implemented by using the parallel eccentricity
    implementation.

    networkx.periphery : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.periphery.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """
    if e is None:
        e = eccentricity(G, get_chunks=get_chunks)
    d = max(e.values())
    p = [v for v, ecc in e.items() if ecc == d]
    return p
