import networkx as nx
from networkx import DiGraph, Graph, MultiDiGraph, MultiGraph
from .classes.graph import (
    ParallelGraph,
    ParallelDiGraph,
    ParallelMultiDiGraph,
    ParallelMultiGraph,
)
from .algorithms.centrality.betweenness import betweenness_centrality
from .algorithms.isolate import number_of_isolates, isolates, is_isolate
from .algorithms.vitality import closeness_vitality
from .algorithms.tournament import (
    hamiltonian_path,
    is_reachable,
    tournament_is_strongly_connected,
    is_tournament,
    random_tournament,
    score_sequence,
    tournament_matrix,
)
from .algorithms.efficiency_measures import (
    efficiency,
    local_efficiency,
    global_efficiency,
)


__all__ = ["Dispatcher"]


def convert(graph):
    if isinstance(graph, MultiDiGraph):
        return ParallelMultiDiGraph(graph)
    if isinstance(graph, MultiGraph):
        return ParallelMultiGraph(graph)
    if isinstance(graph, DiGraph):
        return ParallelDiGraph(graph)
    if isinstance(graph, Graph):
        return ParallelGraph(graph)
    raise TypeError(f"Unsupported type of graph: {type(graph)}")


class Dispatcher:
    # =============================

    # Isolates
    number_of_isolates = number_of_isolates
    isolates = isolates
    is_isolate = is_isolate

    # Vitality
    closeness_vitality = closeness_vitality

    # Tournament
    is_tournament = is_tournament
    hamiltonian_path = hamiltonian_path
    random_tournament = random_tournament
    score_sequence = score_sequence
    tournament_matrix = tournament_matrix
    is_reachable = is_reachable
    tournament_is_strongly_connected = tournament_is_strongly_connected

    # Centrality
    betweenness_centrality = betweenness_centrality

    # Efficiency
    efficiency = efficiency
    local_efficiency = local_efficiency
    global_efficiency = global_efficiency

    # =============================
    def __getattr__(self, item):
        try:
            return nx.utils.backends._registered_algorithms[item].__wrapped__
        except KeyError:
            raise AttributeError(item) from None

    @staticmethod
    def convert_from_nx(
        graph,
        *,
        edge_attrs=None,
        node_attrs=None,
        preserve_edge_attrs=None,
        preserve_node_attrs=None,
        preserve_graph_attrs=None,
        name=None,
        graph_name=None,
    ):
        if name in {
            # Raise if input graph changes
            "lexicographical_topological_sort",
            "topological_generations",
            "topological_sort",
            # Sensitive tests (iteration order matters)
            "dfs_labeled_edges",
        }:
            return graph
        if not isinstance(graph, Graph):
            if name == "is_partition":
                # May be NodeView
                return graph
            raise TypeError(
                f"Bad type for graph argument {graph_name} in {name}: type(graph)"
            )

        G = graph.__class__()

        if preserve_graph_attrs:
            G.graph.update(graph.graph)

        if preserve_node_attrs:
            G.add_nodes_from(graph.nodes(data=True))
        elif node_attrs:
            G.add_nodes_from(
                (
                    node,
                    {
                        k: datadict.get(k, default)
                        for k, default in node_attrs.items()
                        if default is not None or k in datadict
                    },
                )
                for node, datadict in graph.nodes(data=True)
            )
        else:
            G.add_nodes_from(graph)

        if graph.is_multigraph():
            if preserve_edge_attrs:
                G.add_edges_from(
                    (u, v, key, datadict)
                    for u, nbrs in graph._adj.items()
                    for v, keydict in nbrs.items()
                    for key, datadict in keydict.items()
                )
            elif edge_attrs:
                G.add_edges_from(
                    (
                        u,
                        v,
                        key,
                        {
                            k: datadict.get(k, default)
                            for k, default in edge_attrs.items()
                            if default is not None or k in datadict
                        },
                    )
                    for u, nbrs in graph._adj.items()
                    for v, keydict in nbrs.items()
                    for key, datadict in keydict.items()
                )
            else:
                G.add_edges_from(
                    (u, v, key, {})
                    for u, nbrs in graph._adj.items()
                    for v, keydict in nbrs.items()
                    for key, datadict in keydict.items()
                )
        elif preserve_edge_attrs:
            G.add_edges_from(graph.edges(data=True))
        elif edge_attrs:
            G.add_edges_from(
                (
                    u,
                    v,
                    {
                        k: datadict.get(k, default)
                        for k, default in edge_attrs.items()
                        if default is not None or k in datadict
                    },
                )
                for u, v, datadict in graph.edges(data=True)
            )
        else:
            G.add_edges_from(graph.edges)
        return G

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        return obj
