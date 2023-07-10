from networkx import Graph, DiGraph, MultiDiGraph, MultiGraph

__all__ = ["ParallelGraph", "ParallelDiGraph", "ParallelMultiDiGraph", "ParallelMultiGraph"]


class ParallelGraph(Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return Graph(self)
    
class ParallelDiGraph(DiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return DiGraph(self)
    
class ParallelMultiGraph(Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return MultiGraph(self)
    

class ParallelMultiDiGraph(Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def to_networkx(self):
        return MultiDiGraph(self)