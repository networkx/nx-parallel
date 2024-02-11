from joblib import Parallel, delayed
from networkx.algorithms.bipartite.redundancy import _node_redundancy
import networkx as nx
import nx_parallel as nxp


__all__ = ["node_redundancy"]


def node_redundancy(G, nodes=None):
    """Computes the node redundancy coefficients for the nodes in the bipartite
    graph `G`."""
    def compute_node_redundancy(G, v):
        return _node_redundancy(G, v)
    if hasattr(G, "graph_object"):
        G = G.graph_object
    if nodes is None:
        nodes = G
    if any(len(G[v]) < 2 for v in nodes):
        raise nx.NetworkXError(
            "Cannot compute redundancy coefficient for a node"
            " that has fewer than two neighbors."
        )
    total_cores = nxp.cpu_count()
    node_redundancies = Parallel(n_jobs=total_cores)(
        delayed(compute_node_redundancy)(G, v) for v in nodes
    )
    return dict(zip(nodes, node_redundancies))
