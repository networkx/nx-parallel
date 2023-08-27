from networkx import Graph, DiGraph, MultiDiGraph, MultiGraph

__all__ = ["ParallelGraph", "ParallelDiGraph", "ParallelMultiDiGraph", "ParallelMultiGraph"]


class ParallelGraph(Graph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        self.originalGraph = Graph(self)

    def to_networkx(self):
        return Graph(self)
    
class ParallelDiGraph(DiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        self.originalGraph = DiGraph(self)

    def to_networkx(self):
        return DiGraph(self)
    
class ParallelMultiGraph(MultiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        self.originalGraph = MultiGraph(self)

    def to_networkx(self):
        return MultiGraph(self)
    

class ParallelMultiDiGraph(MultiDiGraph):
    __networkx_plugin__ = "parallel"

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        self.originalGraph = MultiDiGraph(self)

    def to_networkx(self):
        return MultiDiGraph(self)