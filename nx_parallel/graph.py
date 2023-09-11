import networkx as nx
from typing import Dict, Optional

__all__ = ["ParallelGraph", "ParallelDiGraph", "ParallelMultiDiGraph", "ParallelMultiGraph"]


class ParallelGraph(nx.Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data: Optional[Dict], **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return nx.Graph(self)


class ParallelDiGraph(nx.DiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data: Optional[Dict], **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return nx.DiGraph(self)


class ParallelMultiGraph(nx.MultiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data: Optional[Dict], **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return nx.MultiGraph(self)


class ParallelMultiDiGraph(nx.MultiDiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data: Optional[Dict], **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return nx.MultiDiGraph(self)


class Converters:
    @staticmethod
    def graph2pargraph(graph: nx.Graph) -> ParallelGraph:
        """Converts NetworkX graph to ParallelGraph."""
        if isinstance(graph, nx.MultiDiGraph):
            return ParallelMultiDiGraph(graph)
        if isinstance(graph, nx.MultiGraph):
            return ParallelMultiGraph(graph)
        if isinstance(graph, nx.DiGraph):
            return ParallelDiGraph(graph)
        if isinstance(graph, nx.Graph):
            return ParallelGraph(graph)
        raise TypeError(f"Unsupported type of graph: {type(graph)}")

    @staticmethod
    def pargraph2graph(G: ParallelGraph) -> nx.Graph:
        if isinstance(G, ParallelMultiDiGraph):
            return ParallelMultiDiGraph.to_networkx(G)
        if isinstance(G, ParallelMultiGraph):
            return ParallelMultiGraph.to_networkx(G)
        if isinstance(G, ParallelDiGraph):
            return ParallelDiGraph.to_networkx(G)
        if isinstance(G, ParallelGraph):
            return ParallelGraph.to_networkx(G)
        raise TypeError(f"Unsupported type of graph: {type(G)}")
