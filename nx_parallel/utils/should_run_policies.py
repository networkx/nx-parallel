def should_skip_parallel(G, *_):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(G, *_):
    if len(G) < 500:
        return "Graph too small for parallel execution"
    return True
