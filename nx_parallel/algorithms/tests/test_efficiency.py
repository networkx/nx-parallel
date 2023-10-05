"""Unit tests for the :mod:`networkx.algorithms.efficiency` module."""

import networkx as nx

import nx_parallel


class TestEfficiency:
    def setup_method(self):
        # G1 is a disconnected graph
        self.G1 = nx.Graph()
        self.G1.add_nodes_from([1, 2, 3])
        self.H1 = nx_parallel.ParallelGraph(self.G1)
        # G2 is a cycle graph
        self.G2 = nx.cycle_graph(4)
        self.H2 = nx_parallel.ParallelGraph(self.G2)
        # G3 is the triangle graph with one additional edge
        self.G3 = nx.lollipop_graph(3, 1)
        self.H3 = nx_parallel.ParallelGraph(self.G3)

    def test_local_efficiency_disconnected_graph(self):
        """
        In a disconnected graph the efficiency is 0
        """
        assert nx.local_efficiency(self.H1) == 0

    def test_local_efficiency_complete_graph(self):
        """
        Test that the local efficiency for a complete graph with at least 3
        nodes should be one. For a graph with only 2 nodes, the induced
        subgraph has no edges.
        """
        for n in range(3, 10):
            G = nx.complete_graph(n)
            H = nx_parallel.ParallelGraph(G)
            assert nx.local_efficiency(H) == 1

    def test_using_ego_graph(self):
        """
        Test that the ego graph is used when computing local efficiency.
        For more information, see GitHub issue #2710.
        """
        assert nx.local_efficiency(self.H3) == 7 / 12
