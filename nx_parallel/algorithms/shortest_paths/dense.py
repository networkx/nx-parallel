"""Floyd-Warshall algorithm for shortest paths."""
from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx
import numpy as np

__all__ = [
    "floyd_warshall_numpy",
]


def floyd_warshall_numpy(G, nodelist=None, weight="weight", get_chunks="chunks"):
    """
    Parallel implementation of Floyd warshall using the tiled floyd warshall algorithm from
    'All-Pairs Shortest-Paths for Large Graphs on the GPU, Authors: Gary J. Katz and Joseph T. Kider Jr'

    networkx.floyd_warshall_numpy : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n` chunks, where `n` is the number of CPU cores.
    """

    if nodelist is not None:
        if not (len(nodelist) == len(G) == len(set(nodelist))):
            raise nxp.NetworkXError(
                "nodelist must contain every node in G with no repeats."
                "If you wanted a subgraph of G use G.subgraph(nodelist)"
            )

    # To handle cases when an edge has weight=0, we must make sure that
    # nonedges are not given the value 0 as well.
    A = nx.to_numpy_array(
        G, nodelist, multigraph_weight=min, weight=weight, nonedge=np.inf
    )
    n, m = A.shape
    (
        k,
        i,
        j,
    ) = 1  # TODO: chunking in submatrix and assign k i j iterable for sub block that are not primary
    # total_cores = nxp.cpu_count()
    # blocking_factor = (
    #    n / total_cores
    # )  # TODO: write a more specific chunking for spliting non dividable matrix

    Parallel(n_jobs=1, require="sharedmem")(
        delayed(_partial_floyd_warshall_numpy)(A, k, i, j) for i in range(10)
    )

    return A


def _partial_floyd_warshall_numpy(A, k_iteration, i_iteration, j_iteration):
    """
    Compute partial FW in the determined sub-block for the execution of
    parallel tiled FW.

    Parameters
    ----------
    A : 2D numpy.ndarray
        matrix that reppresent the adjacency matrix of the graph

    k_iteration : tuple
        range (start-end) of the primary block in the current iteration

    i_iteration : tuple
        range (start-end) of the rows in the current block computed

    j_iteration : tuple
        range (start-end) of the columns in the current block computed

    Returns
    -------
    A : 2D numpy.ndarray
        adjacency matrix updated after floyd warshall
    """

    for k in range(k_iteration[0], k_iteration[1] + 1):
        for i in range(i_iteration[0], i_iteration[1] + 1):
            for j in range(j_iteration[0], j_iteration[1] + 1):
                A[i][j] = np.minimum(A[i][j], (A[i][k] + A[k][j]))
    return A
