"""Floyd-Warshall algorithm for shortest paths."""
from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx
import numpy as np
import math

__all__ = [
    "floyd_warshall_numpy",
]


def floyd_warshall_numpy(G, nodelist=None, weight="weight", blocking_factor=None):
    """
    Parallel implementation of Floyd warshall using the tiled floyd warshall algorithm from
    'All-Pairs Shortest-Paths for Large Graphs on the GPU, Authors: Gary J. Katz and Joseph T. Kider Jr'

    networkx.floyd_warshall_numpy : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.dense.floyd_warshall_numpy.html

    Parameters
    ----------
    blocking_factor : number
        The number used for divinding the adjacency matrix in block.
        The default blocking factor is get by finding the optimal value
        for the core available
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
    matrix_len = m * n

    # TODO: handle graph with a prime number of node, as the matrix is not divisible
    total_cores = nxp.cpu_count()
    if blocking_factor is None:
        blocking_factor = _find_nearest_divisor(n, total_cores)

    no_of_primary = matrix_len / blocking_factor

    for primary_block in range(no_of_primary):
        k_start = (primary_block * matrix_len) // no_of_primary
        k_end = k_start + (matrix_len // no_of_primary) - 1
        k = (k_start, k_end)
        # Phase 1: Compute Primary block
        # Execute Normal floyd warshall for the primary block submatrix
        A = _partial_floyd_warshall_numpy(A, k, k, k)
        # Phase 2: Compute Cross block
        params = []
        for block in range(no_of_primary):
            # skip the primary block computed in phase 1
            if block != primary_block:
                # append the actual indices of the matrix by multiply the block number with the blocking factor
                block_coord = _block_range(blocking_factor, block)
                params.append((block_coord, k))
                params.append((k, block_coord))
        Parallel(n_jobs=(no_of_primary - 1) * 2, require="sharedmem")(
            delayed(_partial_floyd_warshall_numpy)(A, k, i, j) for (i, j) in params
        )
        # Phase 3: Compute remaining
        params.clear()
        for block_i in range(no_of_primary):
            for block_j in range(no_of_primary):
                # skip all block previously computed, so skip every block with primary block value
                if block_i != primary_block and block_j != primary_block:
                    i_range = _block_range(blocking_factor, block_i)
                    j_range = _block_range(blocking_factor, block_j)
                    params.append((i_range, j_range))
        Parallel(n_jobs=(no_of_primary - 1) ** 2, require="sharedmem")(
            delayed(_partial_floyd_warshall_numpy)(A, k, i, j) for (i, j) in params
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


def _block_range(blocking_factor, block):
    return (block * blocking_factor, (block + 1) * blocking_factor)


def _calculate_divisor(i, x, y):
    if x % i == 0:
        divisor1 = i
        result1 = x // i
        difference1 = abs((result1 - 1) ** 2 - y)

        divisor2 = x // i
        result2 = i
        difference2 = abs((result2 - 1) ** 2 - y)

        if difference1 < difference2:
            return divisor1, result1, difference1
        else:
            return divisor2, result2, difference2
    return None


# TODO add side case for prime number
def _find_nearest_divisor(x, y):
    """
    find the optimal value for the blocking factor parameter

    Parameters
    ----------
    x : node number

    y : cpu core available
    """
    # Find the square root of x
    sqrt_x = int(math.sqrt(x)) + 1

    # Execute the calculation in parallel
    results = Parallel(n_jobs=-1)(
        delayed(_calculate_divisor)(i, x, y) for i in range(1, sqrt_x)
    )

    # Filter out None results
    results = [r for r in results if r is not None]

    # Find the best divisor
    best_divisor, best_result, min_difference = min(results, key=lambda x: x[2])

    return best_divisor
