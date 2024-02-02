from nx_parallel.algorithms.centrality.betweenness import betweenness_centrality_chunk, betweenness_centrality_no_chunk
from nx_parallel.algorithms.shortest_paths.weighted import all_pairs_bellman_ford_path_chunk, all_pairs_bellman_ford_path_no_chunk
from nx_parallel.algorithms.efficiency_measures import local_efficiency_chunk, local_efficiency_no_chunk
from nx_parallel.algorithms.isolate import number_of_isolates_chunk, number_of_isolates_no_chunk
from nx_parallel.algorithms.tournament import (
    is_reachable_chunk,
    is_reachable_no_chunk,
    is_strongly_connected_chunk,
    is_strongly_connected_no_chunk,
)
from nx_parallel.algorithms.vitality import closeness_vitality_chunk, closeness_vitality_no_chunk

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
    number_of_isolates_chunk = number_of_isolates_chunk
    number_of_isolates_no_chunk = number_of_isolates_no_chunk

    # Vitality
    closeness_vitality_chunk = closeness_vitality_chunk
    closeness_vitality_no_chunk = closeness_vitality_no_chunk

    # Tournament
    is_reachable_chunk = is_reachable_chunk
    is_reachable_no_chunk = is_reachable_no_chunk
    tournament_is_strongly_connected_chunk = is_strongly_connected_chunk
    tournament_is_strongly_connected_no_chunk = is_strongly_connected_no_chunk

    # Centrality
    betweenness_centrality_chunk = betweenness_centrality_chunk
    betweenness_centrality_no_chunk = betweenness_centrality_no_chunk

    # Efficiency
    local_efficiency_chunk = local_efficiency_chunk
    local_efficiency_no_chunk = local_efficiency_no_chunk

    # Shortest Paths : all pairs shortest paths(bellman_ford)
    all_pairs_bellman_ford_path_chunk = all_pairs_bellman_ford_path_chunk
    all_pairs_bellman_ford_path_no_chunk = all_pairs_bellman_ford_path_no_chunk

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
