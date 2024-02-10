"""Provides functions for computing the efficiency of nodes and graphs."""
import networkx as nx
from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["local_efficiency"]


def local_efficiency(G):
    """The parallel computation is implemented by dividing the
    nodes into chunks and then computing and adding global efficiencies of all node
    in all chunks, in parallel, and then adding all these sums and dividing by the
    total number of nodes at the end.

    networkx.local_efficiency : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.efficiency_measures.local_efficiency.html#local-efficiency
    """

    def _local_efficiency_node_subset(G, nodes):
        return sum(nx.global_efficiency(G.subgraph(G[v])) for v in nodes)

    if hasattr(G, "graph_object"):
        G = G.graph_object

    cpu_count = nxp.cpu_count()

    num_in_chunk = max(len(G.nodes) // cpu_count, 1)
    node_chunks = list(nxp.chunks(G.nodes, num_in_chunk))

    efficiencies = Parallel(n_jobs=cpu_count)(
        delayed(_local_efficiency_node_subset)(G, chunk) for chunk in node_chunks
    )
    return sum(efficiencies) / len(G)
