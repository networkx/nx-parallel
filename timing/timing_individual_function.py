import timeit
import random
import types

import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import nx_parallel as nxp


def execFunc(func, *args, **kwargs):
    c = func(*args, **kwargs)
    if isinstance(c, types.GeneratorType):
        d = dict(c)
    return d


# Code to create README heatmaps for individual function currFun
heatmapDF = pd.DataFrame()
# for bipartite graphs
# n = [50, 100, 200, 400]
# m = [25, 50, 100, 200]
nodes = [75, 150, 300, 600]
weighted = False
pList = [1, 0.8, 0.6, 0.4, 0.2]
currFun = nx.all_pairs_bellman_ford_path_length
for p in pList:
    for num in nodes:
        # create original and parallel graphs
        G = nx.fast_gnp_random_graph(num, p, seed=42, directed=True)

        """
        # for bipartite.node_redundancy
        G = nx.bipartite.random_graph(n[num], m[num], p, seed=42, directed=True)
        for i in G.nodes:
            l = list(G.neighbors(i))
            if len(l) == 0:
                v = random.choice(list(G.nodes) - [i,])
                G.add_edge(i, v)
                G.add_edge(i, random.choice([node for node in G.nodes if node != i]))
            elif len(l) == 1:
                G.add_edge(i, random.choice([node for node in G.nodes if node != i and node not in list(G.neighbors(i))]))
        """

        # for weighted graphs
        if weighted:
            random.seed(42)
            for u, v in G.edges():
                G[u][v]["weight"] = random.random()

        H = nxp.ParallelGraph(G)

        # time both versions and update heatmapDF
        parallelTime = timeit.timeit(lambda: execFunc(currFun, H), number=1)
        stdTime = timeit.timeit(lambda: execFunc(currFun, G), number=1)
        timesFaster = stdTime / parallelTime
        heatmapDF.at[num, p] = timesFaster
        print("Finished " + str(currFun))

# Code to create for row of heatmap specifically for tournaments
# for p in pList:
#     for num in nodes:
#         G = nx.tournament.random_tournament(num)
#         H = nx_parallel.ParallelDiGraph(G)
#         parallelTime = timeit.timeit(lambda: nx.tournament.is_reachable(H, 1, num), number=1)
#         stdTime = timeit.timeit(lambda: nx.tournament.is_reachable(G, 1, num), number=1)
#         timesFaster = stdTime / parallelTime
#         timesFaster = stdTime/parallelTime
#         heatmapDF.at[num, 3] = timesFaster

# plotting the heatmap with numbers and a green color scheme
plt.figure(figsize=(20, 4))
hm = sns.heatmap(data=heatmapDF.T, annot=True, cmap="Greens", cbar=True)

# Remove the tick labels on both axes
hm.set_yticklabels(pList)

# Adding x-axis labels
hm.set_xticklabels(nodes)

# Rotating the x-axis labels for better readability (optional)
plt.xticks(rotation=45)
plt.yticks(rotation=20)
plt.title(
    "Small Scale Demo: Times Speedups of " + currFun.__name__ + " compared to NetworkX"
)
plt.xlabel("Number of Vertices")
plt.ylabel("Edge Probability")
print(currFun.__name__)

# displaying the plotted heatmap
plt.tight_layout()
plt.savefig("timing/" + "heatmap_" + currFun.__name__ + "_timing.png")
