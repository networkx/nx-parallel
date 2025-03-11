from joblib import Parallel, delayed
import networkx as nx
import networkx.utils as nxu
import networkx.parallel as nxp

__all__ = ["voterank_parallel"]

@nxp._configure_if_nx_active()
@nxu.py_random_state(5)
def voterank_parallel(
    G,
    number_of_nodes=None,
    get_chunks="chunks",
):
    """Parallelized VoteRank Algorithm using joblib.

    This implementation splits the graph into chunks and processes each chunk
    in parallel using joblib. It follows the approach used in betweenness
    centrality parallelization.

    Parameters
    ----------
    G : networkx.Graph
        Input graph.
    number_of_nodes : int, optional
        Number of ranked nodes to extract (default: all nodes).
    get_chunks : str, function (default = "chunks")
        A function that takes in a list of all the nodes as input and returns
        an iterable `node_chunks`. The default chunking is done by slicing the
        `nodes` into `n_jobs` number of chunks.

    Returns
    -------
    influential_nodes : list
        List of influential nodes ranked by VoteRank.
    """

    if hasattr(G, "graph_object"):
        G = G.graph_object

    if len(G) == 0:
        return []

    # Set default number of nodes to rank
    if number_of_nodes is None or number_of_nodes > len(G):
        number_of_nodes = len(G)

    # Get number of parallel jobs
    n_jobs = nxp.get_n_jobs()

    # Determine chunks of nodes for parallel processing
    nodes = list(G.nodes())
    if get_chunks == "chunks":
        node_chunks = nxp.create_iterables(G, "node", n_jobs, nodes)
    else:
        node_chunks = get_chunks(nodes)

    # Initialize vote ranking structure
    vote_rank = {n: [0, 1] for n in G.nodes()}
    avg_degree = sum(deg for _, deg in G.degree()) / len(G)

    def process_chunk(chunk):
        """Process a chunk of nodes and compute VoteRank scores."""
        local_vote_rank = {n: [0, 1] for n in chunk}
        
        for n in chunk:
            local_vote_rank[n][0] = 0  # Reset scores
        for n, nbr in G.edges():
            local_vote_rank[n][0] += vote_rank[nbr][1]
            if not G.is_directed():
                local_vote_rank[nbr][0] += vote_rank[n][1]
        
        return local_vote_rank

    influential_nodes = []

    for _ in range(number_of_nodes):
        # Run parallel processing on node chunks
        vote_chunks = Parallel(n_jobs=n_jobs)(
            delayed(process_chunk)(chunk) for chunk in node_chunks
        )

        # Merge partial results
        for chunk_result in vote_chunks:
            for node, scores in chunk_result.items():
                vote_rank[node][0] += scores[0]

        # Select top influential node
        top_node = max(G.nodes, key=lambda x: vote_rank[x][0])
        if vote_rank[top_node][0] == 0:
            break
        influential_nodes.append(top_node)

        # Weaken the selected node and its neighbors
        vote_rank[top_node] = [0, 0]
        for _, nbr in G.edges(top_node):
            vote_rank[nbr][1] = max(vote_rank[nbr][1] - 1 / avg_degree, 0)

    return influential_nodes

