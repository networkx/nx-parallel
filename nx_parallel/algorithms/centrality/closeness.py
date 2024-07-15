__all__ = ["closeness_centrality"]


def closeness_centrality(
    G, u=None, distance=None, wf_improved=True, get_chunks="chunks"
):
    """The parallel implementation first divide the nodes into chunks and

    networkx.closeness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html

    Parameters
    ----------
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns an
        iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n` chunks, where `n` is the number of CPU cores.
    """
