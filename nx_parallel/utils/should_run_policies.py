import nx_parallel as nxp


__all__ = [
    "default_should_run",
    "should_skip_parallel",
    "should_run_if_large",
    "should_run_if_sparse",
]


def should_skip_parallel(*_, **__):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(nodes_threshold=200, *_, **__):
    # If nodes_threshold is a graph-like object, it's being used as a direct should_run
    # function instead of a factory. Use default threshold.
    if hasattr(nodes_threshold, '__len__') and hasattr(nodes_threshold, 'nodes'):
        # nodes_threshold is actually a graph, use it as G with default threshold
        G = nodes_threshold
        threshold = 200

        if hasattr(G, "graph_object"):
            G = G.graph_object

        if len(G) < threshold:
            return "Graph too small for parallel execution"
        return True

    # Otherwise, it's being used as a factory, return a wrapper
    threshold = nodes_threshold
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
