import nx_parallel as nxp
from nx_parallel.interface import ALGORITHMS
import networkx as nx
import inspect
import pytest


def get_functions_with_should_run():
    for name, obj in inspect.getmembers(nxp.algorithms, inspect.isfunction):
        if callable(obj.should_run):
            yield name


def test_get_functions_with_should_run():
    assert set(get_functions_with_should_run()) == set(ALGORITHMS)


@pytest.mark.parametrize("func_name", get_functions_with_should_run())
def test_should_run(func_name):
    tournament_funcs = [
        "tournament_is_strongly_connected",
    ]

    if func_name in tournament_funcs:
        G = nx.tournament.random_tournament(15, seed=42)
    else:
        G = nx.fast_gnp_random_graph(40, 0.6, seed=42)
    H = nxp.ParallelGraph(G)
    func = getattr(nxp, func_name)

    result = func.should_run(H)
    if not isinstance(result, (bool, str)):
        raise AssertionError(
            f"{func.__name__}.should_run has an invalid return type; {type(result)}"
        )
