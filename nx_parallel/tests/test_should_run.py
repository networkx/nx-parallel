import inspect
import nx_parallel as nxp
from nx_parallel import algorithms
import pytest
import os
import joblib
import networkx as nx
from nx_parallel.interface import ALGORITHMS
from nx_parallel import should_run_if_large, should_skip_parallel


def get_functions_with_should_run():
    for name, obj in inspect.getmembers(algorithms, inspect.isfunction):
        if callable(obj.should_run):
            yield name


def test_get_functions_with_custom_should_run():
    assert set(get_functions_with_should_run()) == set(ALGORITHMS)


def test_default_should_run():
    @nxp._configure_if_nx_active()
    def dummy_default():
        pass

    with pytest.MonkeyPatch().context() as mp:
        mp.delitem(os.environ, "PYTEST_CURRENT_TEST", raising=False)
        assert (
            dummy_default.should_run()
            == "Parallel backend requires `n_jobs` > 1 to run"
        )

        with joblib.parallel_config(n_jobs=4):
            assert dummy_default.should_run()


def test_skip_parallel_backend():
    @nxp._configure_if_nx_active(should_run=should_skip_parallel)
    def dummy_skip_parallel():
        pass

    assert dummy_skip_parallel.should_run() == "Fast algorithm; skip parallel execution"


def test_should_run_if_large():
    @nxp._configure_if_nx_active(should_run=should_run_if_large)
    def dummy_if_large(G):
        pass

    smallG = nx.fast_gnp_random_graph(20, 0.6, seed=42)
    largeG = nx.fast_gnp_random_graph(250, 0.6, seed=42)

    assert dummy_if_large.should_run(smallG) == "Graph too small for parallel execution"
    assert dummy_if_large.should_run(largeG)


@pytest.mark.parametrize("func", get_functions_with_should_run())
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
    if not isinstance(result, (bool, str)):
        raise AssertionError(
            f"{func.__name__}.should_run has an invalid return type; {type(result)}"
        )
