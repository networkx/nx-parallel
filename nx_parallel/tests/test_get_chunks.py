# smoke tests for all functions supporting `get_chunks` kwarg

import inspect
import importlib
import random
import types
import math
import os
import pytest
import networkx as nx

import nx_parallel as nxp


def test_get_n_jobs():
    """Test for various scenarios in `get_n_jobs`."""
    # Test with no n_jobs (default)
    with pytest.MonkeyPatch().context() as mp:
        mp.delitem(os.environ, "PYTEST_CURRENT_TEST", raising=False)
        assert nxp.get_n_jobs() == 1

        # Test with n_jobs set to positive value
        assert nxp.get_n_jobs(4) == 4

        # Test with n_jobs set to negative value
        assert nxp.get_n_jobs(-1) == os.cpu_count()

    # Test with n_jobs = 0 to raise a ValueError
    try:
        nxp.get_n_jobs(0)
    except ValueError as e:
        assert str(e) == "n_jobs == 0 in Parallel has no meaning"


def test_chunks():
    """Test `chunks` for various input scenarios."""
    data = list(range(10))

    # Test chunking with exactly 2 larger chunks (balanced)
    chunks_list = list(nxp.chunks(data, 2))
    assert chunks_list == [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)]

    # Test chunking into 5 smaller chunks
    chunks_list = list(nxp.chunks(data, 5))
    assert chunks_list == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]


def test_create_iterables():
    """Test `create_iterables` for different iterator types."""
    G = nx.fast_gnp_random_graph(50, 0.6, seed=42)

    # Test node iterator
    iterable = nxp.create_iterables(G, nxp.utils.GraphIteratorType.NODE, 4)
    assert len(list(iterable)) == 4

    # Test edge iterator
    iterable = nxp.create_iterables(G, nxp.utils.GraphIteratorType.EDGE, 4)
    assert len(list(iterable)) == 4

    # Test isolate iterator (G has no isolates, so this should be empty)
    iterable = nxp.create_iterables(G, nxp.utils.GraphIteratorType.ISOLATE, 4)
    assert len(list(iterable)) == 0


def get_all_functions(package_name="nx_parallel"):
    """Returns a dict keyed by function names to its arguments.

    This function constructs a dictionary keyed by the function
    names in the package `package_name` to dictionaries containing
    the function's keyword arguments and positional arguments.
    """
    package = importlib.import_module(package_name)
    functions = {}

    for name, obj in inspect.getmembers(package, inspect.isfunction):
        if not name.startswith("_"):
            args, kwargs = inspect.getfullargspec(obj)[:2]
            functions[name] = {"args": args, "kwargs": kwargs}

    return functions


def get_functions_with_get_chunks():
    """Returns a list of function names with the `get_chunks` kwarg."""
    all_funcs = get_all_functions()
    get_chunks_funcs = []
    for func in all_funcs:
        if "get_chunks" in all_funcs[func]["args"]:
            get_chunks_funcs.append(func)
    return get_chunks_funcs


def test_get_chunks():
    def random_chunking(nodes):
        _nodes = list(nodes).copy()
        random.seed(42)
        random.shuffle(_nodes)
        num_chunks = nxp.get_n_jobs()
        num_in_chunk = max(len(_nodes) // num_chunks, 1)
        return nxp.chunks(_nodes, num_in_chunk)

    get_chunks_funcs = get_functions_with_get_chunks()
    ignore_funcs = [
        "number_of_isolates",
        "is_reachable",
    ]
    tournament_funcs = [
        "tournament_is_strongly_connected",
    ]
    chk_dict_vals = [
        "betweenness_centrality",
        "edge_betweenness_centrality",
    ]
    G = nx.fast_gnp_random_graph(50, 0.6, seed=42)
    H = nxp.ParallelGraph(G)
    for func in get_chunks_funcs:
        print(func)
        if func not in ignore_funcs:
            if func in tournament_funcs:
                G = nx.tournament.random_tournament(50, seed=42)
                H = nxp.ParallelGraph(G)
                c1 = getattr(nxp, func)(H)
                c2 = getattr(nxp, func)(H, get_chunks=random_chunking)
                assert c1 == c2
            else:
                c1 = getattr(nxp, func)(H)
                c2 = getattr(nxp, func)(H, get_chunks=random_chunking)
                if isinstance(c1, types.GeneratorType):
                    c1, c2 = dict(c1), dict(c2)
                    if func in chk_dict_vals:
                        for i in range(len(G.nodes)):
                            assert math.isclose(c1[i], c2[i], abs_tol=1e-16)
                    else:
                        assert c1 == c2
                else:
                    if func in chk_dict_vals:
                        for i in range(len(G.nodes)):
                            assert math.isclose(c1[i], c2[i], abs_tol=1e-16)
                    else:
                        if isinstance(c1, float):
                            assert math.isclose(c1, c2, abs_tol=1e-16)
                        else:
                            assert c1 == c2
