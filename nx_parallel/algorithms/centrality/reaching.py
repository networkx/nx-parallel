"""Parallel functions for computing reaching centrality of a node or a graph."""

import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp
from networkx.algorithms.centrality.reaching import _average_weight

__all__ = ["global_reaching_centrality", "local_reaching_centrality"]


def global_reaching_centrality(G, weight=None, normalized=True):
    """Returns the global reaching centrality of a directed graph."""

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if nx.is_negatively_weighted(G, weight=weight):
        raise nx.NetworkXError("edge weights must be positive")
    total_weight = G.size(weight=weight)
    if total_weight <= 0:
        raise nx.NetworkXError("Size of G must be positive")

    if weight is not None:

        def as_distance(u, v, d):
            return total_weight / d.get(weight, 1)

        shortest_paths = nx.shortest_path(G, weight=as_distance)
    else:
        shortest_paths = nx.shortest_path(G)

    centrality = local_reaching_centrality
    total_cores = nxp.cpu_count()
    lrc = Parallel(n_jobs=total_cores)(
        delayed(centrality)(G, node, paths=paths, weight=weight, normalized=normalized)
        for node, paths in dict(shortest_paths).items()
    )

    max_lrc = max(lrc)
    return sum(max_lrc - c for c in lrc) / (len(G) - 1)


def local_reaching_centrality(G, v, paths=None, weight=None, normalized=True):
    """Returns the local reaching centrality of a node in a directed graph."""

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if paths is None:
        if nx.is_negatively_weighted(G, weight=weight):
            raise nx.NetworkXError("edge weights must be positive")
        total_weight = G.size(weight=weight)
        if total_weight <= 0:
            raise nx.NetworkXError("Size of G must be positive")
        if weight is not None:
            # Interpret weights as lengths.
            def as_distance(u, v, d):
                return total_weight / d.get(weight, 1)

            paths = nx.shortest_path(G, source=v, weight=as_distance)
        else:
            paths = nx.shortest_path(G, source=v)
    # If the graph is unweighted, simply return the proportion of nodes
    # reachable from the source node ``v``.
    if weight is None and G.is_directed():
        return (len(paths) - 1) / (len(G) - 1)
    if normalized and weight is not None:
        norm = G.size(weight=weight) / G.size()
    else:
        norm = 1
    total_cores = nxp.cpu_count()
    avgw = Parallel(n_jobs=total_cores)(
        delayed(_average_weight)(G, path, weight=weight) for path in paths.values()
    )
    sum_avg_weight = sum(avgw) / norm
    return sum_avg_weight / (len(G) - 1)
