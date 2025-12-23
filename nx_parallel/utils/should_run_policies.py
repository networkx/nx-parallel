import nx_parallel as nxp


__all__ = [
    "default_should_run",
    "should_skip_parallel",
    "should_run_if_large",
    "should_run_if_nodes_none",
    "should_run_if_sparse",
]


def should_skip_parallel(*_):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(G, *_):
    if hasattr(G, "graph_object"):
        G = G.graph_object

    if len(G) <= 200:
        return "Graph too small for parallel execution"
    return True


def default_should_run(*_):
    n_jobs = nxp.get_n_jobs()
    print(f"{n_jobs=}")
    if n_jobs in (None, 0, 1):
        return "Parallel backend requires `n_jobs` > 1 to run"
    return True


def should_run_if_nodes_none(G, nodes=None, *_):
    if nodes is None:
        return True
    return "Parallel execution only supported when `nodes` is None"


def should_run_if_sparse(threshold=0.3):
    def wrapper(G, *_):
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
