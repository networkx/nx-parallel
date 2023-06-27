from networkx import Graph

__all__ = ["ParallelGraph"]


class ParallelGraph(Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return Graph(self)
