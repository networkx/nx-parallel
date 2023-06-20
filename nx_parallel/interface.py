from .centrality import betweenness_centrality

__all__ = ["Dispatcher"]


class Dispatcher:
    betweenness_centrality = betweenness_centrality

    @staticmethod
    def convert_from_nx(incoming_graph, weight=None, *, name=None):
        import networkx as nx
        from .graph import ParallelGraph

        if isinstance(incoming_graph, nx.Graph):
            return ParallelGraph(incoming_graph)
        raise TypeError(f"Unsupported type of graph: {type(incoming_graph)}")

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        from .graph import ParallelGraph

        if isinstance(obj, Graph):
            obj = obj.to_networkx()
        return obj

    # @staticmethod
    # def on_start_tests(items):
    #     try:
    #         import pytest
    #     except ImportError:  # pragma: no cover (import)
    #         return
    #     skip = [
    #         ("test_attributes", {"TestBoruvka", "test_mst.py"}),
    #         ("test_weight_attribute", {"TestBoruvka", "test_mst.py"}),
    #     ]
    #     for item in items:
    #         kset = set(item.keywords)
    #         for test_name, keywords in skip:
    #             if item.name == test_name and keywords.issubset(kset):
    #                 item.add_marker(
    #                     pytest.mark.xfail(reason="unable to handle multi-attributed graphs")
    #                 )
