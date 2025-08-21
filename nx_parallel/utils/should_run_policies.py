import nx_parallel as nxp


__all__ = [
    "default_should_run",
    "should_skip_parallel",
    "should_run_if_large",
]


def should_skip_parallel(*_):
    return "Fast algorithm; skip parallel execution"


def should_run_if_large(G, *_):
    if len(G) <= 200:
        return "Graph too small for parallel execution"
    return True


def default_should_run(*_):
    n_jobs = nxp.get_n_jobs()
    print(f"{n_jobs=}")
    if n_jobs in (None, 0, 1):
        return "Parallel backend requires `n_jobs` > 1 to run"
    return True
