import inspect
import pytest
import networkx as nx
import nx_parallel as nxp
from nx_parallel import algorithms


def get_functions_with_custom_should_run():
    """Yields names of functions with a custom `should_run`"""

    for name, obj in inspect.getmembers(algorithms, inspect.isfunction):
        if obj.should_run is not True:
            yield name


def test_get_functions_with_custom_should_run():
    expected = {
        "number_of_isolates",
    }
    assert set(get_functions_with_custom_should_run()) == expected


@pytest.mark.parametrize("func", get_functions_with_custom_should_run())
def test_should_run(func):
    # [TO DO]: modify graphs based on whether the func is a tournament
    G = nx.fast_gnp_random_graph(40, 0.6, seed=42)
    H = nxp.ParallelGraph(G)
    func = getattr(nxp, func)

    result = func.should_run(H)
    if not isinstance(result, bool) and not isinstance(result, str):
        raise AssertionError(
            f"{func.__name__}.should_run has an invalid return type; {type(result)}"
        )
