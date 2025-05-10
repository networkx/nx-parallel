# smoke tests for all functions supporting `get_chunks` kwarg

import inspect
import importlib
import random
import types
import math
import networkx as nx

import nx_parallel as nxp


def get_all_funcs_with_args(package_name="nx_parallel"):
    """Returns a dict keyed by function names to a list of
    the function's args names, for all the functions in
    the package `package_name`.
    """
    package = importlib.import_module(package_name)
    funcs_with_args = {}

    for name, obj in inspect.getmembers(package, inspect.isfunction):
        if not name.startswith("_"):
            signature = inspect.signature(obj)
            arguments = [
                param.name
                for param in signature.parameters.values()
                if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ]
            funcs_with_args[name] = arguments
    return funcs_with_args


def get_functions_with_get_chunks():
    """Returns a list of function names with the `get_chunks` kwarg."""
    all_funcs = get_all_funcs_with_args()
    get_chunks_funcs = []
    for func in all_funcs:
        if "get_chunks" in all_funcs[func]:
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
                        for key in c1:
                            assert math.isclose(c1[key], c2[key], abs_tol=1e-16)
                    else:
                        assert c1 == c2
                else:
                    if func in chk_dict_vals:
                        for key in c1:
                            assert math.isclose(c1[key], c2[key], abs_tol=1e-16)
                    else:
                        if isinstance(c1, float):
                            assert math.isclose(c1, c2, abs_tol=1e-16)
                        else:
                            assert c1 == c2
