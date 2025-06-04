"""
Performance analysis of parallel and NetworkX implementations of the input function
"""

from time import perf_counter
import random
import types
import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import nx_parallel as nxp
import joblib

# Default Config
joblib.parallel_config(n_jobs=-1)
# To use NetworkX's parallel backend, set the following configuration.
# nx.config.backends.parallel.active = True
# nx.config.backends.parallel.n_jobs = 6

tournament_funcs = ["is_reachable", "tournament_is_strongly_connected"]
bipartite_funcs = ["node_redundancy"]


def time_individual_function(currFunc, number_of_nodes, edge_prob, *, weighted=False):
    def measure_time(G, *args):
        t1 = perf_counter()
        c1 = currFunc(G, *args)
        if isinstance(c1, types.GeneratorType):
            _ = dict(c1)
        t2 = perf_counter()
        return t2 - t1

    def record_result(stdTime, parallelTime, row, col):
        timesFaster = stdTime / parallelTime
        speedup_df.at[row, col] = timesFaster
        heatmap_annot.at[row, col] = f"{parallelTime:.2g}s\n{timesFaster:.2g}x"

    speedup_df = pd.DataFrame(index=number_of_nodes, columns=edge_prob, dtype=float)
    heatmap_annot = pd.DataFrame(index=number_of_nodes, columns=edge_prob, dtype=object)

    if currFunc.__name__ not in tournament_funcs:
        for p in edge_prob:
            for ind, num in enumerate(number_of_nodes):
                # for bipartite graphs
                if currFunc.__name__ in bipartite_funcs:
                    n = [50, 100, 200, 400]
                    m = [25, 50, 100, 200]
                    print(n[ind] + m[ind])
                    G = nx.bipartite.random_graph(
                        n[ind], m[ind], p, seed=42, directed=True
                    )
                    for cur_node in G.nodes:
                        neighbors = list(G.neighbors(cur_node))
                        # Have atleast 2 outgoing edges
                        if len(neighbors) == 0:
                            G.add_edge(
                                cur_node,
                                random.choice([node for node in G if node != cur_node]),
                            )
                            G.add_edge(
                                cur_node,
                                random.choice(
                                    [
                                        node
                                        for node in G.nodes
                                        if node != cur_node
                                        and node not in list(G.neighbors(cur_node))
                                    ]
                                ),
                            )
                        elif len(neighbors) == 1:
                            G.add_edge(
                                cur_node,
                                random.choice(
                                    [
                                        node
                                        for node in G.nodes
                                        if node != cur_node
                                        and node not in list(G.neighbors(cur_node))
                                    ]
                                ),
                            )
                else:
                    print(num)
                    G = nx.fast_gnp_random_graph(num, p, seed=42, directed=True)

                # for weighted graphs
                if weighted:
                    random.seed(42)
                    for u, v in G.edges():
                        G[u][v]["weight"] = random.random()

                H = nxp.ParallelGraph(G)
                # time both versions and update speedup_df
                parallelTime = measure_time(H)
                print(parallelTime)
                stdTime = measure_time(G)
                print(stdTime)
                record_result(stdTime, parallelTime, number_of_nodes[num], p)
                print("Finished " + str(currFunc))
    else:
        # for tournament graphs
        for num in number_of_nodes:
            print(num)
            G = nx.tournament.random_tournament(num, seed=42)
            H = nxp.ParallelGraph(G)
            parallelTime = measure_time(H, 1, num)
            print(parallelTime)
            stdTime = measure_time(G, 1, num)
            print(stdTime)
            record_result(stdTime, parallelTime, num, edge_prob[0])
            print("Finished " + str(currFunc))
    return (speedup_df, heatmap_annot)


def plot_timing_heatmap(currFunc):
    number_of_nodes = (
        [10, 50, 100, 300, 500]
        if currFunc.__name__ not in bipartite_funcs
        else [75, 150, 300, 600]
    )
    edge_prob = (
        [1, 0.8, 0.6, 0.4, 0.2] if currFunc.__name__ not in tournament_funcs else [1]
    )

    (speedup_df, heatmap_annot) = time_individual_function(
        currFunc, number_of_nodes, edge_prob
    )

    # Plot the heatmap with performance speedup values
    plt.figure(figsize=(20, 4))
    hm = sns.heatmap(
        data=speedup_df.T, annot=heatmap_annot.T, fmt="", cmap="RdYlGn", cbar=True
    )

    # Set tick labels for y-axis (edge probabilities) and x-axis (number of nodes)
    hm.set_xticklabels(number_of_nodes)
    hm.set_yticklabels(edge_prob)

    # Improve readability by rotating axis tick labels
    plt.xticks(rotation=45)
    plt.yticks(rotation=20)
    plt.title(
        "Small Scale Demo: Times Speedups of "
        + currFunc.__name__
        + " compared to NetworkX"
    )
    plt.xlabel("Number of Vertices")
    plt.ylabel("Edge Probability")
    print(currFunc.__name__)

    plt.savefig("timing/" + "heatmap_" + currFunc.__name__ + "_timing.png")


# plot_timing_heatmap(nx.algorithms.centrality.betweenness.betweenness_centrality)
