import inspect
import pytest
import networkx as nx
import nx_parallel as nxp
from nx_parallel import algorithms
import joblib
from nx_parallel.interface import ALGORITHMS


def get_functions_with_custom_should_run():
    """Yields names of functions with a custom `should_run`"""

    for name, obj in inspect.getmembers(algorithms, inspect.isfunction):
        if obj.should_run is not True:
            yield name


def test_get_functions_with_custom_should_run():
    with joblib.parallel_config(n_jobs=4):
        assert set(get_functions_with_custom_should_run()) == set(ALGORITHMS)


@pytest.mark.parametrize("func", get_functions_with_custom_should_run())
def test_should_run(func):
    tournament_funcs = [
        "tournament_is_strongly_connected",
    ]

    if func in tournament_funcs:
        G = nx.tournament.random_tournament(15, seed=42)
    else:
        G = nx.fast_gnp_random_graph(40, 0.6, seed=42)
    H = nxp.ParallelGraph(G)
    func = getattr(nxp, func)

    result = func.should_run(H)
    if not isinstance(result, bool) and not isinstance(result, str):
        raise AssertionError(
            f"{func.__name__}.should_run has an invalid return type; {type(result)}"
        )
