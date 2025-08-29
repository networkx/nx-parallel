import networkx as nx
from nx_parallel import algorithms

__all__ = ["BackendInterface", "ParallelGraph"]


ALGORITHMS = [
    # Bipartite
    "node_redundancy",
    # Isolates
    "number_of_isolates",
    # Vitality
    "closeness_vitality",
    # Tournament
    "is_reachable",
    "tournament_is_strongly_connected",
    # Link Prediction
    "resource_allocation_index",
    "jaccard_coefficient",
    "adamic_adar_index",
    "preferential_attachment",
    "common_neighbor_centrality",
    "cn_soundarajan_hopcroft",
    "ra_index_soundarajan_hopcroft",
    "within_inter_cluster",
    # Centrality
    "betweenness_centrality",
    "edge_betweenness_centrality",
    "harmonic_centrality",
    # Components : attracting
    "number_attracting_components",
    # Components : connected
    "number_connected_components",
    # Components : strongly connected
    "number_strongly_connected_components",
    # Components : weakly connected
    "number_weakly_connected_components",
    # Dag
    "colliders",
    "v_structures",
    # Efficiency
    "local_efficiency",
    # Shortest Paths : generic
    "all_pairs_all_shortest_paths",
    # Shortest Paths : weighted graphs
    "all_pairs_dijkstra",
    "all_pairs_dijkstra_path_length",
    "all_pairs_dijkstra_path",
    "all_pairs_bellman_ford_path_length",
    "all_pairs_bellman_ford_path",
    "johnson",
    # Clustering
    "square_clustering",
    "triangles",
    "clustering",
    "average_clustering",
    # Shortest Paths : unweighted graphs
    "all_pairs_shortest_path",
    "all_pairs_shortest_path_length",
    # Approximation
    "approximate_all_pairs_node_connectivity",
    # Assortativity
    "average_neighbor_degree",
    # Connectivity
    "all_pairs_node_connectivity",
]


class ParallelGraph:
    """A wrapper class for networkx.Graph, networkx.DiGraph, networkx.MultiGraph,
    and networkx.MultiDiGraph.
    """

    __networkx_backend__ = "parallel"

    def __init__(self, graph_object=None):
        if graph_object is None:
            self.graph_object = nx.Graph()
        elif isinstance(graph_object, nx.Graph):
            self.graph_object = graph_object
        else:
            self.graph_object = nx.Graph(graph_object)

    def is_multigraph(self):
        return self.graph_object.is_multigraph()

    def is_directed(self):
        return self.graph_object.is_directed()

    def __str__(self):
        return f"Parallel{self.graph_object}"


class BackendInterface:
    """BackendInterface class for parallel algorithms."""

    @staticmethod
    def convert_from_nx(graph, *args, **kwargs):
        """Convert a networkx.Graph, networkx.DiGraph, networkx.MultiGraph,
        or networkx.MultiDiGraph to a ParallelGraph.
        """
        if isinstance(graph, ParallelGraph):
            return graph
        return ParallelGraph(graph)

    @staticmethod
    def convert_to_nx(result, *, name=None):
        """Convert a ParallelGraph to a networkx.Graph, networkx.DiGraph,
        networkx.MultiGraph, or networkx.MultiDiGraph.
        """
        if isinstance(result, ParallelGraph):
            return result.graph_object
        return result

    @classmethod
    def should_run(cls, name, args, kwargs):
        """Determine whether this backend should run the specified algorithm
        with the given arguments.

        Parameters
        ----------
        cls : type
            `BackendInterface` class
        name : str
            Name of the target algorithm
        args : tuple
            Positional arguments passed to the algorithm's `should_run`.
        kwargs : dict
            Keyword arguments passed to the algorithm's `should_run`.

        Returns
        -------
        bool or str
            If the algorithm should run, returns True.
            Otherwise, returns a string explaining why parallel execution is skipped.
        """
        return getattr(cls, name).should_run(*args, **kwargs)


for attr in ALGORITHMS:
    setattr(BackendInterface, attr, getattr(algorithms, attr))
