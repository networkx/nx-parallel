# smoke tests for all functions supporting `get_chunks` kwarg

import inspect
import importlib
import random
import types
import math

import networkx as nx
import pytest

import nx_parallel as nxp
from nx_parallel.interface import ALGORITHMS


def get_functions_with_get_chunks(ignore_funcs=[], package_name="nx_parallel"):
    """Yields function names for functions with a `get_chunks` kwarg."""

    package = importlib.import_module(package_name)

    for name, obj in inspect.getmembers(package, inspect.isfunction):
        if not name.startswith("_"):
            signature = inspect.signature(obj)
            arguments = [
                param.name
                for param in signature.parameters.values()
                if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ]
            if name not in ignore_funcs and "get_chunks" in arguments:
                yield name


def test_get_functions_with_get_chunks():
    assert set(get_functions_with_get_chunks()) == set(ALGORITHMS)


ignore_funcs = [
    "number_of_isolates",
    "is_reachable",
]


@pytest.mark.parametrize("func", get_functions_with_get_chunks(ignore_funcs))
def test_get_chunks(func):
    def random_chunking(nodes):
        _nodes = list(nodes).copy()
        random.seed(42)
        random.shuffle(_nodes)
        n_jobs = nxp.get_n_jobs()
        return nxp.chunks(_nodes, n_jobs)

    tournament_funcs = [
        "tournament_is_strongly_connected",
    ]
    check_dict_values_close = [
        "betweenness_centrality",
        "edge_betweenness_centrality",
    ]

    if func in tournament_funcs:
        G = nx.tournament.random_tournament(15, seed=42)
        H = nxp.ParallelGraph(G)
        c1 = getattr(nxp, func)(H)
        c2 = getattr(nxp, func)(H, get_chunks=random_chunking)
        assert c1 == c2
    else:
        G = nx.fast_gnp_random_graph(40, 0.6, seed=42)
        H = nxp.ParallelGraph(G)
        c1 = getattr(nxp, func)(H)
        c2 = getattr(nxp, func)(H, get_chunks=random_chunking)
        if isinstance(c1, types.GeneratorType):
            c1, c2 = dict(c1), dict(c2)
            if func in check_dict_values_close:
                for key in c1:
                    assert math.isclose(c1[key], c2[key], abs_tol=1e-16)
            else:
                assert c1 == c2
        else:
            if func in check_dict_values_close:
                for key in c1:
                    assert math.isclose(c1[key], c2[key], abs_tol=1e-16)
            else:
                if isinstance(c1, float):
                    assert math.isclose(c1, c2, abs_tol=1e-16)
                else:
                    assert c1 == c2
