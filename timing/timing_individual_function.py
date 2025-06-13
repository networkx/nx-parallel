"""
Performance analysis of parallel and NetworkX implementations of the input function.

To generate heatmaps for performance visualization, make sure to run:
    python3 -m pip install -e '.[heatmap]'
"""

import timeit
import random
import types
import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import nx_parallel as nxp
import joblib
import numpy as np

# Default Config
joblib.parallel_config(n_jobs=-1)
# To use NetworkX's parallel backend, set the following configuration.
# nx.config.backends.parallel.active = True
# nx.config.backends.parallel.n_jobs = -1

tournament_funcs = ["is_reachable", "tournament_is_strongly_connected"]
bipartite_funcs = ["node_redundancy"]


def time_individual_function(
    targetFunc, number_of_nodes, edge_prob, speedup_df, heatmap_annot, *, weighted=False
):
    def measure_time(G, *args):
        def wrapper():
            result = targetFunc(G, *args)
            if isinstance(result, types.GeneratorType):
                _ = dict(result)

        times = timeit.repeat(wrapper, repeat=5, number=1)
        return min(times)

    def record_result(stdTime, parallelTime, row, col):
        timesFaster = stdTime / parallelTime
        speedup_df.at[row, col] = timesFaster
        heatmap_annot.at[row, col] = f"{parallelTime:.2g}s\n{timesFaster:.2g}x"

    if targetFunc.__name__ not in tournament_funcs:
        for p in edge_prob:
            for ind, num in enumerate(number_of_nodes):
                # for bipartite graphs
                if targetFunc.__name__ in bipartite_funcs:
                    n = [200, 400, 800, 1600]
                    m = [100, 200, 400, 800]
                    print(n[ind] + m[ind])
                    G = nx.bipartite.random_graph(
                        n[ind], m[ind], p, seed=42, directed=True
                    )
                    for cur_node in G.nodes:
                        neighbors = set(G.neighbors(cur_node))
                        # Have atleast 2 outgoing edges
                        while len(neighbors) < 2:
                            new_neighbor = random.choice(
                                [
                                    node
                                    for node in G.nodes
                                    if node != cur_node and node not in neighbors
                                ]
                            )
                            G.add_edge(cur_node, new_neighbor)
                            neighbors.add(new_neighbor)
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
                record_result(stdTime, parallelTime, num, p)
                print("Finished " + str(targetFunc))
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
            print("Finished " + str(targetFunc))


def plot_timing_heatmap(targetFunc):
    number_of_nodes = (
        [200, 400, 800, 1600]
        if targetFunc.__name__ not in bipartite_funcs
        else [300, 600, 1200, 2400]
    )
    edge_prob = (
        [1, 0.8, 0.6, 0.4, 0.2] if targetFunc.__name__ not in tournament_funcs else [1]
    )

    speedup_df = pd.DataFrame(index=number_of_nodes, columns=edge_prob, dtype=float)
    heatmap_annot = pd.DataFrame(index=number_of_nodes, columns=edge_prob, dtype=object)

    time_individual_function(
        targetFunc, number_of_nodes, edge_prob, speedup_df, heatmap_annot
    )

    # Plot the heatmap with performance speedup values
    plt.figure(figsize=(20, 4))
    sns.heatmap(
        data=speedup_df.T, annot=heatmap_annot.T, fmt="", cmap="Greens", cbar=True
    )

    plt.xticks(
        ticks=np.arange(len(number_of_nodes)) + 0.5, labels=number_of_nodes, rotation=45
    )
    plt.yticks(ticks=np.arange(len(edge_prob)) + 0.5, labels=edge_prob, rotation=20)

    plt.title(
        "Small Scale Demo: Times Speedups of "
        + targetFunc.__name__
        + " compared to NetworkX for n_jobs="
        + str(nxp.get_n_jobs())
    )
    plt.xlabel("Number of Vertices")
    plt.ylabel("Edge Probability")
    print(targetFunc.__name__)

    plt.savefig("timing/" + "heatmap_" + targetFunc.__name__ + "_timing.png")


plot_timing_heatmap(nx.algorithms.tournament.is_reachable)
