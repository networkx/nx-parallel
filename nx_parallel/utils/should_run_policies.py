import nx_parallel as nxp


__all__ = [
    "default_should_run",
    "should_skip_parallel",
    "should_run_if_large",
    "should_run_if_sparse",
]


def should_skip_parallel(*_, **__):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(G=None, nodes_threshold=200, *_, **__):
    # Detect if first arg is a graph (has both __len__ and nodes attributes)
    is_graph = G is not None and hasattr(G, '__len__') and hasattr(G, 'nodes')
    
    if is_graph:
        # Direct usage: called with a graph as first argument
        # Example: should_run_if_large(G) or func.should_run(G)
        if hasattr(G, "graph_object"):
            G = G.graph_object

        if len(G) < nodes_threshold:
            return "Graph too small for parallel execution"
        return True
    
    # Factory usage: called with threshold (positional or keyword) but no graph
    # Examples: should_run_if_large(50000) or should_run_if_large(nodes_threshold=50000)
    # Use G if it's a number (threshold passed positionally), otherwise use nodes_threshold
    threshold = G if G is not None and isinstance(G, (int, float)) else nodes_threshold
    
    def wrapper(G, *_, **__):
        if hasattr(G, "graph_object"):
            G = G.graph_object

        if len(G) < threshold:
            return "Graph too small for parallel execution"
        return True

    return wrapper


def default_should_run(*_, **__):
    n_jobs = nxp.get_n_jobs()
    print(f"{n_jobs=}")
    if n_jobs in (None, 0, 1):
        return "Parallel backend requires `n_jobs` > 1 to run"
    return True


def should_run_if_sparse(threshold=0.3):
    def wrapper(G, *_, **__):
        if hasattr(G, "graph_object"):
            G = G.graph_object

        nodes = len(G)
        # Handle trivial graphs separately to avoid division by zero
        if nodes <= 1:
            return "Empty graph" if nodes == 0 else "Single-node graph"

        density = 2 * G.number_of_edges() / (nodes * (nodes - 1))
        return (
            True
            if density <= threshold
            else "Graph too dense to benefit from parallel execution"
        )

    return wrapper
