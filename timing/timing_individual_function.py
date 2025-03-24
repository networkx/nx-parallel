import time
import networkx as nx
import nx_parallel as nxp
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# Code to create README heatmaps for individual function currFun
heatmapDF = pd.DataFrame()
number_of_nodes_list = [10, 50, 100, 200, 400]
pList = [1, 0.8, 0.6, 0.4, 0.2]  # List of edge probabilities
currFun = nxp.degree_centrality

for p in pList:  # Loop through edge probabilities
    for num in number_of_nodes_list:  # Loop through number of nodes
        print(f"Processing graph with {num} nodes and edge probability {p}")

        # Create original and parallel graphs
        G = nx.fast_gnp_random_graph(num, p, seed=42, directed=True)
        H = nxp.ParallelGraph(G)

        # Time the parallel version
        t1 = time.time()
        c1 = currFun(H)
        t2 = time.time()
        parallelTime = t2 - t1

        # Time the standard version
        t1 = time.time()
        c2 = currFun(G)
        t2 = time.time()
        stdTime = t2 - t1

        # Calculate speedup
        timesFaster = stdTime / parallelTime
        heatmapDF.at[num, p] = timesFaster
        print(f"Finished {currFun.__name__} for {num} nodes and p={p}")

# Plotting the heatmap with numbers and a green color scheme
plt.figure(figsize=(20, 4))
hm = sns.heatmap(data=heatmapDF.T, annot=True, cmap="Greens", cbar=True)

# Adding x-axis and y-axis labels
hm.set_xticklabels(number_of_nodes_list)
hm.set_yticklabels(pList)

# Rotating the x-axis labels for better readability
plt.xticks(rotation=45)
plt.yticks(rotation=20)
plt.title(
    f"Speedups of {currFun.__name__} compared to NetworkX for Different Edge Probabilities"
)
plt.xlabel("Number of Vertices")
plt.ylabel("Edge Probability")

# Save and display the heatmap
plt.tight_layout()
plt.savefig(f"heatmap_{currFun.__name__}_timing.png")
plt.show()
