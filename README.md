# nx-parallel

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance.

## Features

nx-parallel provides parallelized implementations for the following NetworkX functions:

- [betweeness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L17)
- [local_efficiency](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/efficiency_measures.py#L12)
- [number_of_isolates](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/isolate.py#L9)
- [all_pairs_bellman_ford_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L9)
- [is_reachable](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L11)
- [tournament_is_strongly_connected](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L103)
- [closeness_vitality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/vitality.py#L9)

![alt text](timing/heatmap_all_functions.png)

See the `/timing` folder for more heatmaps and code for heatmap generation!

## Usage

Here's an example of how to use nx-parallel:

```python
import networkx as nx
import nx_parallel as nxp

G = nx.path_graph(4)
H = nxp.ParallelGraph(G)

nx.betweenness_centrality(G, backend="parallel") # method 1 : using the backend kwarg
nx.betweenness_centrality(H) # method 2 : passing ParallelGraph object in networkx function
nxp.betweenness_centrality(G) # method 3 : using nx-parallel function with networkx object
nxp.betweenness_centrality(H) # method 4 : using nx-parallel function with ParallelGraph object

# output : {0: 0.0, 1: 0.6666666666666666, 2: 0.6666666666666666, 3: 0.0}
```
