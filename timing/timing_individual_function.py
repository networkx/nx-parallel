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
# To use NetworkX's parallel backend directly, uncomment:
# nx.config.backends.parallel.active = True
# nx.config.backends.parallel.n_jobs = 6

heatmapDF = pd.DataFrame()
number_of_nodes = [10, 50, 100, 300, 500]
tournament_funcs = ["is_reachable", "tournament_is_strongly_connected"]
bipartite_funcs = ["node_redundancy"]
weighted = False
edge_prob = [1, 0.8, 0.6, 0.4, 0.2]
currFun = nx.algorithms.centrality.betweenness.betweenness_centrality

if currFun.__name__ not in tournament_funcs:
    for p in edge_prob:
        for num in range(len(number_of_nodes)):
            print(number_of_nodes[num])
            # create original and parallel graphs
            G = nx.fast_gnp_random_graph(
                number_of_nodes[num], p, seed=42, directed=True
            )

            # for bipartite graphs
            if currFun.__name__ in bipartite_funcs:
                n = [50, 100, 200, 400]
                m = [25, 50, 100, 200]
                G = nx.bipartite.random_graph(n[num], m[num], p, seed=42, directed=True)
                for i in G.nodes:
                    neighbors = list(G.neighbors(i))
                    if len(neighbors) == 0:
                        v = random.choice(
                            list(G.nodes)
                            - [
                                i,
                            ]
                        )
                        G.add_edge(i, v)
                        G.add_edge(
                            i, random.choice([node for node in G.nodes if node != i])
                        )
                    elif len(neighbors) == 1:
                        G.add_edge(
                            i,
                            random.choice(
                                [
                                    node
                                    for node in G.nodes
                                    if node != i and node not in list(G.neighbors(i))
                                ]
                            ),
                        )

            # for weighted graphs
            if weighted:
                random.seed(42)
                for u, v in G.edges():
                    G[u][v]["weight"] = random.random()

            H = nxp.ParallelGraph(G)
            # time both versions and update heatmapDF
            t1 = perf_counter()
            c1 = currFun(H)
            if isinstance(c1, types.GeneratorType):
                d = dict(c1)
            t2 = perf_counter()
            parallelTime = t2 - t1
            print(parallelTime)
            t1 = perf_counter()
            c2 = currFun(G)
            if isinstance(c2, types.GeneratorType):
                d = dict(c2)
            t2 = perf_counter()
            stdTime = t2 - t1
            print(stdTime)
            timesFaster = stdTime / parallelTime
            heatmapDF.at[number_of_nodes[num], p] = timesFaster
            print("Finished " + str(currFun))
else:
    # Code to create for row of heatmap specifically for tournaments
    for num in number_of_nodes:
        print(num)
        G = nx.tournament.random_tournament(num, seed=42)
        H = nxp.ParallelGraph(G)
        t1 = perf_counter()
        c = currFun(H, 1, num)
        t2 = perf_counter()
        parallelTime = t2 - t1
        print(parallelTime)
        t1 = perf_counter()
        c = currFun(G, 1, num)
        t2 = perf_counter()
        stdTime = t2 - t1
        print(stdTime)
        timesFaster = stdTime / parallelTime
        heatmapDF.at[num, 3] = timesFaster
        print("Finished " + str(currFun))


# Plot the heatmap with performance speedup values
plt.figure(figsize=(20, 4))
hm = sns.heatmap(data=heatmapDF.T, annot=True, cmap="RdYlGn", cbar=True)

# Set tick labels for y-axis (edge probabilities) and x-axis (number of nodes)
hm.set_yticklabels(edge_prob)
hm.set_xticklabels(number_of_nodes)

# Improve readability by rotating axis tick labels
plt.xticks(rotation=45)
plt.yticks(rotation=20)

plt.title(
    "Small Scale Demo: Times Speedups of " + currFun.__name__ + " compared to NetworkX"
)
plt.xlabel("Number of Vertices")
plt.ylabel("Edge Probability")
print(currFun.__name__)

# Display the plotted heatmap
plt.tight_layout()
plt.savefig("timing/" + "heatmap_" + currFun.__name__ + "_timing.png")
