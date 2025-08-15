from .common import (
    backends,
    num_nodes,
    Benchmark,
)
import networkx as nx


class DAG(Benchmark):
    params = [backends, num_nodes]
    param_names = ["backend", "num_nodes"]

    def setup(self, backend, num_nodes):
        self.G = nx.gn_graph(num_nodes, seed=42, create_using=nx.DiGraph)

    def time_colliders(self, backend, num_nodes):
        _ = nx.dag.colliders(self.G, backend=backend)

    def time_v_structures(self, backend, num_nodes):
        _ = nx.dag.v_structures(self.G, backend=backend)
