import nx_parallel as nxp
from nx_parallel.interface import ALGORITHMS
import networkx as nx
import inspect
import pytest
import os


def get_functions_with_should_run():
    for name, obj in inspect.getmembers(nxp.algorithms, inspect.isfunction):
        if callable(obj.should_run):
            yield name


def test_get_functions_with_should_run():
    assert set(get_functions_with_should_run()) == set(ALGORITHMS)


def test_default_should_run():
    @nxp._configure_if_nx_active()
    def dummy_default():
        pass

    with pytest.MonkeyPatch().context() as mp:
        mp.delitem(os.environ, "PYTEST_CURRENT_TEST", raising=False)
        with nx.config.backends.parallel(n_jobs=1):
            assert (
                dummy_default.should_run()
                == "Parallel backend requires `n_jobs` > 1 to run"
            )

        assert dummy_default.should_run()


def test_skip_parallel_backend():
    @nxp._configure_if_nx_active(should_run=nxp.should_skip_parallel)
    def dummy_skip_parallel():
        pass

    assert dummy_skip_parallel.should_run() == "Fast algorithm; skip parallel execution"


def test_should_run_if_large():
    @nxp._configure_if_nx_active(should_run=nxp.should_run_if_large)
    def dummy_if_large(G):
        pass

    smallG = nx.fast_gnp_random_graph(20, 0.6, seed=42)
    largeG = nx.fast_gnp_random_graph(250, 0.6, seed=42)

    assert dummy_if_large.should_run(smallG) == "Graph too small for parallel execution"
    assert dummy_if_large.should_run(largeG)


def test_should_run_if_nodes_none():
    @nxp._configure_if_nx_active(should_run=nxp.should_run_if_nodes_none)
    def dummy_nodes_none(G, nodes=None):
        pass

    G = nx.fast_gnp_random_graph(20, 0.6, seed=42)
    assert (
        dummy_nodes_none.should_run(G, nodes=[1, 3])
        == "`nodes` should be None for parallel execution"
    )
    assert dummy_nodes_none.should_run(G)


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
