from joblib import Parallel, delayed
import nx_parallel as nxp

__all__ = ["voterank_centrality"]


def _compute_votes(G, vote_rank, nodes):
    """Compute votes for a chunk of nodes in parallel."""
    votes = {n: 0 for n in nodes}

    for n in nodes:
        for nbr in G[n]:
            votes[n] += vote_rank[nbr][1]  # Node receives votes from neighbors

    return votes


def _update_voting_ability(G, vote_rank, selected_node, avgDegree):
    """Update the voting ability of the selected node and its out-neighbors."""
    for nbr in G[selected_node]:
        vote_rank[nbr][1] = max(
            vote_rank[nbr][1] - (1 / avgDegree), 0
        )  # Ensure non-negative


@nxp._configure_if_nx_active()
def voterank_centrality(G, number_of_nodes=None, *, backend=None, **backend_kwargs):
    """Parallelized VoteRank centrality using joblib with chunking."""
    influential_nodes = []
    vote_rank = {n: [0, 1] for n in G.nodes()}  # (score, voting ability)

    if len(G) == 0:
        return influential_nodes
    if number_of_nodes is None or number_of_nodes > len(G):
        number_of_nodes = len(G)

    avgDegree = sum(
        deg for _, deg in (G.out_degree() if G.is_directed() else G.degree())
    ) / len(G)
    nodes = list(G.nodes())
    chunk_size = backend_kwargs.get("chunk_size", 100)  # Support chunk size override
    node_chunks = [nodes[i : i + chunk_size] for i in range(0, len(nodes), chunk_size)]

    for _ in range(number_of_nodes):
        # Step 1: Compute votes in parallel using chunks
        vote_chunks = Parallel(n_jobs=-1)(
            delayed(_compute_votes)(G, vote_rank, chunk) for chunk in node_chunks
        )

        # Merge chunk results
        votes = {n: 0 for n in G.nodes()}
        for chunk_votes in vote_chunks:
            for node, score in chunk_votes.items():
                votes[node] += score

        # Step 2: Reset votes for already selected nodes
        for n in influential_nodes:
            votes[n] = 0

        # Step 3: Select the most influential node
        n = max(sorted(G.nodes()), key=lambda x: votes[x])  # Deterministic tie-breaking
        if votes[n] == 0:
            return influential_nodes  # Stop if no influential node found

        influential_nodes.append(n)
        vote_rank[n] = [0, 0]  # Weaken selected node

        # Step 4: Update voting ability
        _update_voting_ability(G, vote_rank, n, avgDegree)

    return influential_nodes
