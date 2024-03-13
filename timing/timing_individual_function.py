import time
import random
import types

import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import nx_parallel as nxp

# Code to create README heatmaps for individual function currFun
heatmapDF = pd.DataFrame()
# for bipartite graphs
# n = [50, 100, 200, 400]
# m = [25, 50, 100, 200]
number_of_nodes_list = [75, 150, 300, 600]
weighted = False
pList = [1, 0.8, 0.6, 0.4, 0.2]
currFun = nx.bipartite.node_redundancy
currFun = nx.square_clustering
for p in pList:
    for num in range(len(number_of_nodes_list)):
        # create original and parallel graphs
        G = nx.fast_gnp_random_graph(
            number_of_nodes_list[num], p, seed=42, directed=True
        )

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
        t1 = time.time()
        c1 = currFun(H)
        if isinstance(c1, types.GeneratorType):
            d = dict(c1)
        t2 = time.time()
        parallelTime = t2 - t1
        t1 = time.time()
        c2 = currFun(G)
        if isinstance(c2, types.GeneratorType):
            d = dict(c2)
        t2 = time.time()
        stdTime = t2 - t1
        timesFaster = stdTime / parallelTime
        heatmapDF.at[number_of_nodes_list[num], p] = timesFaster
        print("Finished " + str(currFun))

# Code to create for row of heatmap specifically for tournaments
# for p in pList:
#     for num in number_of_nodes_list):
#         G = nx.tournament.random_tournament(num)
#         H = nx_parallel.ParallelDiGraph(G)
#         t1 = time.time()
#         c = nx.tournament.is_reachable(H, 1, num)
#         t2 = time.time()
#         parallelTime = t2-t1
#         t1 = time.time()
#         c = nx.tournament.is_reachable(G, 1, num)
#         t2 = time.time()
#         stdTime = t2-t1
#         timesFaster = stdTime/parallelTime
#         heatmapDF.at[num, 3] = timesFaster

# plotting the heatmap with numbers and a green color scheme
plt.figure(figsize=(20, 4))
hm = sns.heatmap(data=heatmapDF.T, annot=True, cmap="Greens", cbar=True)

# Remove the tick labels on both axes
hm.set_yticklabels(pList)

# Adding x-axis labels
hm.set_xticklabels(number_of_nodes_list)

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
