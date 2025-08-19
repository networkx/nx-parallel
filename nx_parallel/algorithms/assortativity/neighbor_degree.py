import networkx as nx
import nx_parallel as nxp
from joblib import Parallel, delayed


__all__ = ["average_neighbor_degree"]


@nxp._configure_if_nx_active(nxp.should_skip_parallel)
def average_neighbor_degree(
    G, source="out", target="out", nodes=None, weight=None, get_chunks="chunks"
):
    """The nodes are chunked into `node_chunks` and then the average degree of the
    neighborhood of each node for all `node_chunks` is computed in parallel over
    `n_jobs` number of CPU cores.

    networkx.average_neighbor_degree: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.assortativity.average_neighbor_degree.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes (or nbunch) as input and
        returns an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _process_chunk(source_degree, chunk):
        avg = {}
        for n, deg in source_degree(chunk, weight=weight):
            if deg == 0:
                avg[n] = 0.0
                continue

            if weight is None:
                avg[n] = (
                    sum(t_deg[nbr] for nbr in G_S[n])
                    + sum(t_deg[nbr] for nbr in G_P[n])
                ) / deg
            else:
                avg[n] = (
                    sum(dd.get(weight, 1) * t_deg[nbr] for nbr, dd in G_S[n].items())
                    + sum(dd.get(weight, 1) * t_deg[nbr] for nbr, dd in G_P[n].items())
                ) / deg
        return avg

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if G.is_directed():
        if source == "in":
            source_degree = G.in_degree
        elif source == "out":
            source_degree = G.out_degree
        elif source == "in+out":
            source_degree = G.degree
        else:
            raise nx.NetworkXError(
                f"source argument {source} must be 'in', 'out' or 'in+out'"
            )

        if target == "in":
            target_degree = G.in_degree
        elif target == "out":
            target_degree = G.out_degree
        elif target == "in+out":
            target_degree = G.degree
        else:
            raise nx.NetworkXError(
                f"target argument {target} must be 'in', 'out' or 'in+out'"
            )
    else:
        if source != "out" or target != "out":
            raise nx.NetworkXError(
                "source and target arguments are only supported for directed graphs"
            )
        source_degree = target_degree = G.degree

    t_deg = dict(target_degree())

    G_P = G_S = {n: {} for n in G}
    if G.is_directed():
        if "in" in source:
            G_P = G.pred
        if "out" in source:
            G_S = G.succ
    else:
        G_S = G.adj

    if nodes is None:
        nodes = list(G)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(nodes, n_jobs)
    else:
        node_chunks = get_chunks(nodes)

    results = Parallel()(
        delayed(_process_chunk)(source_degree, chunk) for chunk in node_chunks
    )

    avg = {}
    for result in results:
        avg.update(result)

    return avg
