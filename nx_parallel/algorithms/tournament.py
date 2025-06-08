from joblib import Parallel, delayed, dump, load
import nx_parallel as nxp
import networkx as nx
import numpy as np
import tempfile
import shutil
import os

__all__ = [
    "is_reachable",
    "tournament_is_strongly_connected",
]


@nxp._configure_if_nx_active()
def is_reachable(G, s, t, get_chunks="chunks"):
    """The function parallelizes the calculation of two
    neighborhoods of vertices in `G` and checks closure conditions for each
    neighborhood subset in parallel.

    networkx.tournament.is_reachable : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_reachable.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """

    def two_neighborhood_close(adjM_filepath, chunk):
        adjM = load(adjM_filepath, mmap_mode="r")
        tnc = []
        for v in chunk:
            S = {
                x
                for x in (range(adjM.shape[0]))
                if x == v
                or adjM[v, x]
                or any(adjM[v, z] and adjM[z, x] for z in range(adjM.shape[0]))
            }
            tnc.append(not (is_closed(adjM, S) and s in S and t not in S))
        return all(tnc)

    def is_closed(adjM, nodes):
        other_nodes = set(range(adjM.shape[0])) - nodes
        return all(adjM[u, v] for u in other_nodes for v in nodes)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    adjM = nx.to_numpy_array(G, dtype=np.uint8)
    temp_folder = tempfile.mkdtemp()
    adjM_filepath = os.path.join(temp_folder, "adjMatrix.mmap")
    dump(adjM, adjM_filepath)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(G, n_jobs)
    else:
        node_chunks = get_chunks(G)

    results = Parallel()(
        delayed(two_neighborhood_close)(adjM_filepath, chunk) for chunk in node_chunks
    )
    shutil.rmtree(temp_folder)
    return all(results)


@nxp._configure_if_nx_active()
def tournament_is_strongly_connected(G, get_chunks="chunks"):
    """The parallel computation is implemented by dividing the
    nodes into chunks and then checking whether each node is reachable from each
    other node in parallel.

    Note, this function uses the name `tournament_is_strongly_connected` while
    dispatching to the backend implementation. So, `nxp.tournament.is_strongly_connected`
    will result in an error. Use `nxp.tournament_is_strongly_connected` instead.

    networkx.tournament.is_strongly_connected : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tournament.is_strongly_connected.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the `nodes`
        into `n_jobs` number of chunks.
    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    def is_reachable_subset(G, chunk):
        return all(nx.tournament.is_reachable(G, u, v) for v in chunk for u in G)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(G, n_jobs)
    else:
        node_chunks = get_chunks(G)

    results = Parallel()(
        delayed(is_reachable_subset)(G, chunk) for chunk in node_chunks
    )
    return all(results)
