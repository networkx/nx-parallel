from joblib import Parallel, delayed
import networkx as nx
import nx_parallel as nxp
from functools import partial

__all__ = ["harmonic_centrality"]


@nxp._configure_if_nx_active(should_run=nxp.should_run_if_sparse(threshold=0.3))
def harmonic_centrality(
    G, nbunch=None, distance=None, sources=None, get_chunks="chunks"
):
    """The parallel computation is implemented by dividing the nodes into chunks and
    computing harmonic centrality for each chunk concurrently.

    networkx.harmonic_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.harmonic_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.
    """

    def _process_chunk(chunk):
        hc = {}
        for v in chunk:
            dist = spl(v)
            for u, d_uv in dist.items():
                if d_uv != 0 and u in nbunch:
                    node = v if transposed else u
                    hc[node] = (hc[node] + 1 / d_uv) if node in hc else (1 / d_uv)
        return hc

    if hasattr(G, "graph_object"):
        G = G.graph_object

    nbunch = set(G.nbunch_iter(nbunch))
    sources = set(G.nbunch_iter(sources))

    transposed = False
    if len(nbunch) < len(sources):
        transposed = True
        nbunch, sources = sources, nbunch
        if nx.is_directed(G):
            G = nx.reverse(G, copy=False)

    n_jobs = nxp.get_n_jobs()

    if get_chunks == "chunks":
        node_chunks = nxp.chunks(sources, n_jobs)
    else:
        node_chunks = get_chunks(sources)

    spl = partial(nx.shortest_path_length, G, weight=distance)
    results = Parallel()(delayed(_process_chunk)(chunk) for chunk in node_chunks)

    harmonic = dict.fromkeys(nbunch, 0)
    for result in results:
        for node, c in result.items():
            harmonic[node] += c

    return harmonic
