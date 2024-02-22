from joblib import Parallel, delayed
from networkx.algorithms.shortest_paths.weighted import single_source_bellman_ford_path
import nx_parallel as nxp

__all__ = [
    "all_pairs_bellman_ford_path",
]


def all_pairs_bellman_ford_path(G, weight="weight"):
    """This parallel implementation first creates a generator to lazily compute
    shortest paths for each node, and then employs joblib's `Parallel` function
    to execute these computations in parallel across all available CPU cores.

    networkx.all_pairs_bellman_ford_path : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.all_pairs_bellman_ford_path.html#all-pairs-bellman-ford-path
    """

    def _process_node(source):
        return (source, single_source_bellman_ford_path(G, source, weight=weight))

    if hasattr(G, "graph_object"):
        G = G.graph_object

    paths_generator = (delayed(_process_node)(source) for source in G.nodes)

    for path in Parallel(n_jobs=nxp.cpu_count())(paths_generator):
        yield path
