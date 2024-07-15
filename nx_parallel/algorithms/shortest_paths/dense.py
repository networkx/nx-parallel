"""Floyd-Warshall algorithm for shortest paths."""

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


def _partial_floyd_warshall_numpy(A, k, i, j):
    """
    Compute partial FW in the determined sub-block for the execution of
    parallel tiled FW.

    Parameters
    ----------
    A : 2D numpy.ndarray
        matrix that reppresent the adjacency matrix of the graph

    k : tuple
        range (start-end) of the primary block in the current iteration

    i : tuple
        range (start-end) of the rows in the current block computed

    j : tuple
        range (start-end) of the columns in the current block computed

    Returns
    -------
    A : 2D numpy.ndarray
        adjacency matrix updated after floyd warshall
    """

    # np.add.outer(A[:,k],A[k,:])
