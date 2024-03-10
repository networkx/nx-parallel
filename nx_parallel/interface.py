from nx_parallel.algorithms.centrality.betweenness import betweenness_centrality
from nx_parallel.algorithms.shortest_paths.weighted import (
    all_pairs_bellman_ford_path,
    johnson,
)
from nx_parallel.algorithms.efficiency_measures import local_efficiency
from nx_parallel.algorithms.isolate import number_of_isolates
from nx_parallel.algorithms.tournament import (
    is_reachable,
    tournament_is_strongly_connected,
)
from nx_parallel.algorithms.vitality import closeness_vitality

__all__ = ["Dispatcher", "ParallelGraph"]


class ParallelGraph:
    """A wrapper class for networkx.Graph, networkx.DiGraph, networkx.MultiGraph,
    and networkx.MultiDiGraph."""

    __networkx_backend__ = "parallel"

    def __init__(self, graph_object):
        self.graph_object = graph_object

    def is_multigraph(self):
        return self.graph_object.is_multigraph()

    def is_directed(self):
        return self.graph_object.is_directed()


class Dispatcher:
    """Dispatcher class for parallel algorithms."""

    # Isolates
    number_of_isolates = number_of_isolates

    # Vitality
    closeness_vitality = closeness_vitality

    # Tournament
    is_reachable = is_reachable
    tournament_is_strongly_connected = tournament_is_strongly_connected

    # Centrality
    betweenness_centrality = betweenness_centrality

    # Efficiency
    local_efficiency = local_efficiency

    # Shortest Paths : all pairs shortest paths(bellman_ford)
    all_pairs_bellman_ford_path = all_pairs_bellman_ford_path
    johnson = johnson

    # =============================

    @staticmethod
    def convert_from_nx(
        graph,
        edge_attrs=None,
        node_attrs=None,
        preserve_edge_attrs=False,
        preserve_node_attrs=False,
        preserve_graph_attrs=False,
        name=None,
        graph_name=None,
        *,
        weight=None,  # For nx.__version__ <= 3.1
    ):
        """Convert a networkx.Graph, networkx.DiGraph, networkx.MultiGraph,
        or networkx.MultiDiGraph to a ParallelGraph."""
        if isinstance(graph, ParallelGraph):
            return graph
        return ParallelGraph(graph)

    @staticmethod
    def convert_to_nx(result, *, name=None):
        """Convert a ParallelGraph to a networkx.Graph, networkx.DiGraph,
        networkx.MultiGraph, or networkx.MultiDiGraph."""
        return result
