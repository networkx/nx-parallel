import networkx as nx
from typing import Dict, Optional
from nx_parallel.algorithms.centrality import betweenness_centrality_parallel
from nx_parallel.algorithms.isolate import number_of_isolates_parallel, isolates, is_isolate

__all__ = ["Dispatcher"]

class Dispatcher:
    """Dispatcher for parallel NetworkX algorithms.
    """
    betweenness_centrality = betweenness_centrality_parallel

    isolates = isolates
    is_isolate = is_isolate
    number_of_isolates = number_of_isolates_parallel


    @classmethod
    def convert_from_nx(
        cls,
        graph: nx.Graph,
        *,
        edge_attrs: Optional[Dict] = None,
        node_attrs: Optional[Dict] = None,
        preserve_edge_attrs: Optional[Dict] = None,
        preserve_node_attrs: Optional[Dict] = None,
        preserve_graph_attrs: Optional[Dict] = None,
        name: Optional[str] = None,
        graph_name: Optional[str] = None,
    ) -> nx.Graph:
        if name in {
            # Raise if input graph changes
            "lexicographical_topological_sort",
            "topological_generations",
            "topological_sort",
            # Sensitive tests (iteration order matters)
            "dfs_labeled_edges",
        }:
            return graph
        if not isinstance(graph, nx.Graph):
            if "is_partition" in name:
                return graph
            raise TypeError(
                f"Bad type for graph argument {graph_name} in {name}: {type(graph)}"
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
            cls._convert_multigraph_edges(G, graph, edge_attrs, preserve_edge_attrs)
        else:
            cls._convert_simple_graph_edges(G, graph, edge_attrs, preserve_edge_attrs)

        return G

    @staticmethod
    def _convert_multigraph_edges(G, graph, edge_attrs, preserve_edge_attrs):
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

    @staticmethod
    def _convert_simple_graph_edges(G, graph, edge_attrs, preserve_edge_attrs):
        if preserve_edge_attrs:
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
