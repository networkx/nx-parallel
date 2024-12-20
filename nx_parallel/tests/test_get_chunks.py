import inspect
import importlib
import random
import types
import math
import networkx as nx

import nx_parallel as nxp


def get_all_functions(package_name="nx_parallel.algorithms"):
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
    for func, params in all_funcs.items():
        if "get_chunks" in params["args"]:
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

    # Define a simple process_func for testing
    def process_func(G, chunk, **kwargs):
        # Example: Return the degree of each node in the chunk
        return {node: G.degree(node) for node in chunk}

    # Define a simple iterator_func for testing
    def iterator_func(G):
        return G.nodes()

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
        if func not in ignore_funcs:
            if func in tournament_funcs:
                G = nx.tournament.random_tournament(50, seed=42)
                H = nxp.ParallelGraph(G)
                c1 = getattr(nxp, func)(H, process_func, iterator_func)
                c2 = getattr(nxp, func)(
                    H, process_func, iterator_func, get_chunks=random_chunking
                )
                assert c1 == c2
            else:
                c1 = getattr(nxp, func)(H, process_func, iterator_func)
                c2 = getattr(nxp, func)(
                    H, process_func, iterator_func, get_chunks=random_chunking
                )
                if isinstance(c1, types.GeneratorType):
                    c1, c2 = (
                        list(c1),
                        list(c2),
                    )  # Convert generators to lists for comparison
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
