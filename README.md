## nx_parallel

A NetworkX backend plugin which uses joblib and multiprocessing for parallelization.

```python
In [1]: import networkx as nx; import nx_parallel

In [2]: G = nx.erdos_renyi_graph(10, 0.5)

In [3]: H = nx_parallel.ParallelGraph(G)

In [4]: nx.betweenness_centrality(H)
Out[4]:
{0: 0.0,
 1: 0.0,
 2: 0.0,
 3: 0.0,
 4: 0.0,
 5: 0.0,
 6: 0.0,
 7: 0.0,
 8: 0.0,
 9: 0.0}

```

Currently the following functions have parallelized implementations:

- centrality
  - betweenness_centrality
- tournament
  - is_reachable
- closeness_vitality
- efficiency_measures
  - local_efficiency

![alt text](timing/heatmap_all_functions.png)

See the `/timing` folder for more heatmaps and code for heatmap generation!
