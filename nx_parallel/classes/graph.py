__all__ = ["ParallelGraph"]


class ParallelGraph:
    __networkx_plugin__ = "parallel"

    def __init__(self, graph_object):
        self.graph_object = graph_object
