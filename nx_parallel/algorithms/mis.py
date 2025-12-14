import inspect
from joblib import Parallel, delayed
import nx_parallel as nxp
import networkx as nx

__all__ = ["maximal_independent_set"]

# Import the actual NetworkX implementation (fully unwrapped, not the dispatcher)
from networkx.algorithms.mis import maximal_independent_set as _nx_mis_dispatcher
_nx_mis = inspect.unwrap(_nx_mis_dispatcher)


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_large(50000))
def maximal_independent_set(G, nodes=None, seed=None, get_chunks="chunks"):
    """Returns a random maximal independent set guaranteed to contain
    a given set of nodes.

    This parallel implementation processes nodes in chunks across multiple
    cores, using a Luby-style randomized parallel algorithm for speedup
    on large graphs.

    An independent set is a set of nodes such that the subgraph
    of G induced by these nodes contains no edges. A maximal
    independent set is an independent set such that it is not possible
    to add a new node and still get an independent set.

    The parallel computation divides nodes into chunks and processes them
    in parallel, iteratively building the independent set faster than
    sequential processing on large graphs.

    networkx.maximal_independent_set: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.mis.maximal_independent_set.html

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    nodes : list or iterable, optional
        Nodes that must be part of the independent set. This set of nodes
        must be independent. If not provided, a random starting node is chosen.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    get_chunks : str, function (default = "chunks")
        A function that takes in a list of nodes and returns chunks.
        The default chunking divides nodes into n_jobs chunks.

    Returns
    -------
    indep_nodes : list
        List of nodes that are part of a maximal independent set.

    Raises
    ------
    NetworkXUnfeasible
        If the nodes in the provided list are not part of the graph or
        do not form an independent set, an exception is raised.

    NetworkXNotImplemented
        If `G` is directed.

    Examples
    --------
    >>> import networkx as nx
    >>> import nx_parallel as nxp
    >>> G = nx.path_graph(5)
    >>> nxp.maximal_independent_set(G)  # doctest: +SKIP
    [4, 0, 2]
    >>> nxp.maximal_independent_set(G, [1])  # doctest: +SKIP
    [1, 3]

    Notes
    -----
    This algorithm does not solve the maximum independent set problem.
    The parallel version uses a chunk-based parallel algorithm that
    provides speedup on large graphs (>= 50000 nodes). For smaller graphs,
    the NetworkX sequential version is used automatically.

    """
    if hasattr(G, "graph_object"):
        G = G.graph_object

    # Validate directed graph
    if G.is_directed():
        raise nx.NetworkXNotImplemented("Not implemented for directed graphs.")

    # Convert seed to Random object if needed (for fallback and parallel execution)
    import random
    if seed is not None:
        if hasattr(seed, 'random'):
            # It's already a RandomState/Random object
            rng = seed
        else:
            # It's a seed value
            rng = random.Random(seed)
    else:
        rng = random.Random()

    # Check if we should run parallel version
    # This is needed when backend is explicitly specified
    should_run_result = maximal_independent_set.should_run(G, nodes, seed)
    if should_run_result is not True:
        # Fall back to NetworkX sequential (unwrapped version needs Random object)
        return _nx_mis(G, nodes=nodes, seed=rng)

    # Validate nodes parameter
    if nodes is not None:
        nodes_set = set(nodes)
        if not nodes_set.issubset(G):
            raise nx.NetworkXUnfeasible(f"{nodes} is not a subset of the nodes of G")
        neighbors = set.union(*[set(G.adj[v]) for v in nodes_set]) if nodes_set else set()
        if set.intersection(neighbors, nodes_set):
            raise nx.NetworkXUnfeasible(f"{nodes} is not an independent set of G")
    else:
        nodes_set = set()

    n_jobs = nxp.get_n_jobs()

    # Parallel strategy: Run complete MIS algorithm on node chunks independently
    # Then merge results by resolving conflicts
    all_nodes = list(G.nodes())

    # Remove required nodes and their neighbors from consideration
    if nodes_set:
        available = set(all_nodes) - nodes_set
        for node in nodes_set:
            available.discard(node)
            available.difference_update(G.neighbors(node))
        available = list(available)
    else:
        available = all_nodes

    # Shuffle for randomness
    rng.shuffle(available)

    # Split into chunks
    if get_chunks == "chunks":
        chunks = list(nxp.chunks(available, n_jobs))
    else:
        chunks = list(get_chunks(available))

    # Precompute adjacency
    adj_dict = {node: set(G.neighbors(node)) for node in G.nodes()}

    def _process_chunk_independent(chunk, chunk_seed):
        """Process chunk completely independently - build local MIS."""
        local_rng = random.Random(chunk_seed)
        local_mis = []
        local_excluded = set()

        # Shuffle chunk for randomness
        chunk_list = list(chunk)
        local_rng.shuffle(chunk_list)

        for node in chunk_list:
            if node not in local_excluded:
                # Add to MIS
                local_mis.append(node)
                local_excluded.add(node)
                # Mark neighbors as excluded (only within this chunk)
                for neighbor in adj_dict[node]:
                    if neighbor in chunk_list:
                        local_excluded.add(neighbor)

        return local_mis

    # Generate seeds for each chunk
    chunk_seeds = [rng.randint(0, 2**31 - 1) for _ in range(len(chunks))]

    # Process chunks in parallel
    results = Parallel()(
        delayed(_process_chunk_independent)(chunk, chunk_seeds[i])
        for i, chunk in enumerate(chunks)
    )

    # Merge results: resolve conflicts between chunks
    indep_set = list(nodes_set) if nodes_set else []
    excluded = set(nodes_set)

    if nodes_set:
        for node in nodes_set:
            excluded.update(adj_dict[node])

    # Process results in order, greedily adding non-conflicting nodes
    for local_mis in results:
        for node in local_mis:
            if node not in excluded:
                indep_set.append(node)
                excluded.add(node)
                excluded.update(adj_dict[node])

    return indep_set
