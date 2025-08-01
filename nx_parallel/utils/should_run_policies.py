import nx_parallel as nxp


def should_skip_parallel(*_):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(G, *_):
    if len(G) <= 200:
        return "Graph too small for parallel execution"
    return True


def default_should_run(*_):
    n_jobs = nxp.get_n_jobs()
    if n_jobs in (None, 0, 1):
        return "Set `n_jobs` > 1 to use the parallel backend."
    return True
