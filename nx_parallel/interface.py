from nx_parallel.algorithms.bipartite.redundancy import node_redundancy
from nx_parallel.algorithms.centrality.betweenness import betweenness_centrality
from nx_parallel.algorithms.shortest_paths.generic import all_pairs_all_shortest_paths
from nx_parallel.algorithms.shortest_paths.weighted import (
    all_pairs_dijkstra,
    all_pairs_dijkstra_path_length,
    all_pairs_dijkstra_path,
    all_pairs_bellman_ford_path_length,
    all_pairs_bellman_ford_path,
    johnson,
)
from nx_parallel.algorithms.shortest_paths.unweighted import (
    all_pairs_shortest_path,
    all_pairs_shortest_path_length,
)
from nx_parallel.algorithms.efficiency_measures import local_efficiency
from nx_parallel.algorithms.isolate import number_of_isolates
from nx_parallel.algorithms.tournament import (
    is_reachable,
    tournament_is_strongly_connected,
)
from nx_parallel.algorithms.vitality import closeness_vitality
from nx_parallel.algorithms.approximation.connectivity import (
    approximate_all_pairs_node_connectivity,
)
from nx_parallel.algorithms.connectivity import connectivity
from nx_parallel.algorithms.cluster import square_clustering

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

    # Bipartite
    node_redundancy = node_redundancy

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

    # Shortest Paths : generic
    all_pairs_all_shortest_paths = all_pairs_all_shortest_paths

    # Shortest Paths : weighted graphs
    all_pairs_dijkstra = all_pairs_dijkstra
    all_pairs_dijkstra_path_length = all_pairs_dijkstra_path_length
    all_pairs_dijkstra_path = all_pairs_dijkstra_path
    all_pairs_bellman_ford_path_length = all_pairs_bellman_ford_path_length
    all_pairs_bellman_ford_path = all_pairs_bellman_ford_path
    johnson = johnson

    # Clustering
    square_clustering = square_clustering

    # Shortest Paths : unweighted graphs
    all_pairs_shortest_path = all_pairs_shortest_path
    all_pairs_shortest_path_length = all_pairs_shortest_path_length

    # Approximation
    approximate_all_pairs_node_connectivity = approximate_all_pairs_node_connectivity

    # Connectivity
    all_pairs_node_connectivity = connectivity.all_pairs_node_connectivity

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
