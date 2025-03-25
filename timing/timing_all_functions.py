import time
import os

import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import nx_parallel

# Code to create README heatmap for all functions in function_list
heatmapDF = pd.DataFrame()
function_list = [
    nx.betweenness_centrality,
    nx.closeness_vitality,
    nx.closeness_centrality,
    nx.degree_centrality,
]
number_of_nodes_list = [10, 20, 50, 150, 250]

for i in range(0, len(function_list)):
    currFun = function_list[i]
    for j in range(0, len(number_of_nodes_list)):
        num = number_of_nodes_list[j]

        # create original and parallel graphs
        G = nx.fast_gnp_random_graph(num, 0.5, directed=False)
        H = nx_parallel.ParallelGraph(G)

        # time both versions and update heatmapDF
        t1 = time.time()
        if currFun == nx_parallel.closeness_centrality:
            # Explicitly pass get_chunks="chunks" for the parallel version
            c = currFun(H, get_chunks="chunks")
        else:
            c = currFun(H)
        t2 = time.time()
        parallelTime = t2 - t1

        t1 = time.time()
        if currFun == nx_parallel.closeness_centrality:
            # Explicitly pass get_chunks="chunks" for the parallel version
            c = currFun(G, get_chunks="chunks")
        else:
            c = currFun(G)
        t2 = time.time()
        stdTime = t2 - t1

        timesFaster = stdTime / parallelTime
        heatmapDF.at[j, i] = timesFaster
        print("Finished " + str(currFun))

# Code to handle nx.tournament.is_reachable separately
for j in range(0, len(number_of_nodes_list)):
    num = number_of_nodes_list[j]
    G = nx.tournament.random_tournament(num)
    H = nx_parallel.ParallelGraph(G)
    t1 = time.time()
    c = nx.tournament.is_reachable(
        H, 0, num - 1
    )  # Provide source (0) and target (num - 1)
    t2 = time.time()
    parallelTime = t2 - t1
    t1 = time.time()
    c = nx.tournament.is_reachable(
        G, 0, num - 1
    )  # Provide source (0) and target (num - 1)
    t2 = time.time()
    stdTime = t2 - t1
    timesFaster = stdTime / parallelTime
    heatmapDF.at[j, len(function_list)] = (
        timesFaster  # Add this as a new row in the heatmap
    )
    print("Finished nx.tournament.is_reachable")

# plotting the heatmap with numbers and a green color scheme
plt.figure(figsize=(20, 4))
hm = sns.heatmap(data=heatmapDF.T, annot=True, cmap="Greens", cbar=True)

# Dynamically set y-axis labels based on the number of rows in heatmapDF
labels = [
    "betweenness_centrality",
    "closeness_vitality",
    "degree_centrality",
    "tournament is_reachable",
]

# Ensure the number of labels matches the number of rows in heatmapDF
hm.set_yticklabels(labels[: len(heatmapDF.columns)])

# Adding x-axis labels
hm.set_xticklabels(number_of_nodes_list)

# Rotating the x-axis labels for better readability (optional)
plt.xticks(rotation=45)
plt.yticks(rotation=20)
plt.title("Small Scale Demo: Times Speedups of nx_parallel compared to networkx")
plt.xlabel("Number of Vertices (edge probability of 0.5 except for tournaments)")
plt.ylabel("Algorithm")

# displaying the plotted heatmap
plt.tight_layout()

os.makedirs("timing", exist_ok=True)
plt.savefig("timing/" + "heatmap_all_functions_timing.png")
