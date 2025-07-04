"""
To generate heatmaps comparing the performance of nx-parallel and NetworkX implementations, make sure to run:
    python3 -m pip install -e '.[heatmap]'
"""

import networkx as nx
import nx_parallel as nxp
from matplotlib import pyplot as plt, patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
import joblib
import timeit
import random
import types

# Default Config
joblib.parallel_config(n_jobs=-1)
# To use NetworkX's parallel backend, set the following configuration.
# nx.config.backends.parallel.active = True
# nx.config.backends.parallel.n_jobs = -1

tournament_funcs = ["is_reachable", "tournament_is_strongly_connected"]
bipartite_funcs = ["node_redundancy"]
random.seed(42)


def time_individual_function(
    targetFunc, number_of_nodes, edge_prob, speedup_df, heatmap_annot, *, weighted=False
):
    def measure_time(G, *args):
        repeat = 5

        def wrapper():
            result = targetFunc(G, *args)
            if isinstance(result, types.GeneratorType):
                _ = dict(result)

        times = timeit.repeat(wrapper, repeat=repeat, number=1)
        return min(times)

    def record_result(stdTime, parallelTime, row, col):
        timesFaster = stdTime / parallelTime
        speedup_df.at[row, col] = timesFaster
        heatmap_annot.at[row, col] = f"{parallelTime:.2g}s\n\n{timesFaster:.2g}x"

    if targetFunc.__name__ not in tournament_funcs:
        for p in edge_prob:
            for ind, num in enumerate(number_of_nodes):
                # for bipartite graphs
                if targetFunc.__name__ in bipartite_funcs:
                    n = [200, 400, 800, 1600]
                    m = [100, 200, 400, 800]
                    print(n[ind] + m[ind])
                    G = nx.bipartite.random_graph(n[ind], m[ind], p, directed=True)
                    for cur_node in G.nodes:
                        neighbors = set(G.neighbors(cur_node))
                        # have atleast 2 outgoing edges
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
                    G = nx.fast_gnp_random_graph(num, p, directed=True)

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
            G = nx.tournament.random_tournament(num)
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

    plt.rcParams["font.family"] = "Arial Rounded MT Bold"
    plt.figure(figsize=(20, 6))
    ax = sns.heatmap(
        data=speedup_df.T,
        annot=heatmap_annot.T,
        annot_kws={"size": 12, "weight": "bold"},
        fmt="",
        cmap="Greens",
        cbar=True,
    )

    ax.set_xticks(np.arange(len(number_of_nodes)) + 0.5)
    ax.set_xticklabels(number_of_nodes, rotation=45)
    ax.set_yticks(np.arange(len(edge_prob)) + 0.5)
    ax.set_yticklabels(edge_prob, rotation=20)

    ax.set_xlabel("Number of Vertices", fontweight="bold", fontsize=12)
    ax.set_ylabel("Edge Probability", fontweight="bold", fontsize=12)

    n_jobs = nxp.get_n_jobs()
    ax.set_title(
        f"Small Scale Demo: Time Speedups of {targetFunc.__name__} compared to NetworkX on {n_jobs} cores",
        fontweight="bold",
        fontsize=14,
        loc="left",
    )

    legend_patches = [
        mpatches.Patch(color="none", label="Top Line: Parallel runtime (s)"),
        mpatches.Patch(color="none", label="Bottom Line: Speed-up"),
    ]
    ax.legend(
        handles=legend_patches,
        loc="lower right",
        bbox_to_anchor=(1.0, 1.02),
        title="Cell Annotation Format",
        prop={"size": 12, "weight": "bold"},
    )

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig("timing/" + "heatmap_" + targetFunc.__name__ + "_timing.png")


# plot_timing_heatmap(nx.algorithms.tournament.is_reachable)
