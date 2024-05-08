# smoke tests for all functions supporting `get_chunks` kwarg

import inspect
import importlib
import networkx as nx
import nx_parallel as nxp
import random
import types


def get_all_functions(package_name="nx_parallel"):
    """Returns a dictionary where the keys are the function names in a given Python package, and the values are dictionaries containing the function's keyword arguments and positional arguments."""
    package = importlib.import_module(package_name)
    functions = {}

    for name, obj in inspect.getmembers(package, inspect.isfunction):
        if not name.startswith("_"):
            args, kwargs = inspect.getfullargspec(obj)[:2]
            functions[name] = {"args": args, "kwargs": kwargs}

    return functions


def get_functions_with_get_chunks():
    """Returns a list of functions with the `get_chunks` kwarg."""
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
        num_chunks = nxp.cpu_count()
        num_in_chunk = max(len(_nodes) // num_chunks, 1)
        return nxp.chunks(_nodes, num_in_chunk)

    get_chunks_funcs = get_functions_with_get_chunks()
    ignore_funcs = [
        "betweenness_centrality",
        "is_reachable",
        "local_efficiency",
        "tournament_is_strongly_connected",
    ]
    G = nx.fast_gnp_random_graph(50, 0.6, seed=42)
    H = nxp.ParallelGraph(G)
    for func in get_chunks_funcs:
        if func not in ignore_funcs:
            print(func)
            c1 = getattr(nxp, func)(H)
            c2 = getattr(nxp, func)(H, get_chunks=random_chunking)
            if isinstance(c1, types.GeneratorType):
                assert dict(c1) == dict(c2)
            else:
                assert c1 == c2
