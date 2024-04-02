# nx-parallel

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance.

## Algorithms in nx-parallel

- [number_of_isolates](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/isolate.py#L8)
- [square_clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L10)
- [local_efficiency](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/efficiency_measures.py#L9)
- [closeness_vitality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/vitality.py#L9)
- [is_reachable](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L10)
- [tournament_is_strongly_connected](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L54)
- [all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/connectivity/connectivity.py#L17)
- [approximate_all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/approximation/connectivity.py#L12)
- [betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L16)
- [node_redundancy](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/bipartite/redundancy.py#L11)
- [all_pairs_dijkstra](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L28)
- [all_pairs_dijkstra_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L71)
- [all_pairs_dijkstra_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L121)
- [all_pairs_bellman_ford_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L164)
- [all_pairs_bellman_ford_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L209)
- [johnson](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L252)
- [all_pairs_all_shortest_paths](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/generic.py#L10)
- [all_pairs_shortest_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L18)
- [all_pairs_shortest_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L62)

<details>
<summary>Script used to generate the above list</summary>
  
```.py
import _nx_parallel as nxp
d = nxp.get_funcs_info() # temporarily add `from .update_get_info import *` to _nx_parallel/__init__.py
for func in d:
    print(f"- [{func}]({d[func]['url']})")
```

</details>

## Backend usage

```.py
import networkx as nx
import nx_parallel as nxp

G = nx.path_graph(4)
H = nxp.ParallelGraph(G)

# method 1 : passing ParallelGraph object in networkx function
nx.betweenness_centrality(H)

# method 2 : using the 'backend' kwarg
nx.betweenness_centrality(G, backend="parallel")

# method 3 : using nx-parallel implementation with networkx object
nxp.betweenness_centrality(G)

# method 4 : using nx-parallel implementation with ParallelGraph object
nxp.betweenness_centrality(H)

# output : {0: 0.0, 1: 0.6666666666666666, 2: 0.6666666666666666, 3: 0.0}
```

### Notes

1. Some functions in networkx have the same name but different implementations, so to avoid these name conflicts we differentiate them by the `name` parameter in `_dispatchable` at the time of dispatching (ref. [docs](https://networkx.org/documentation/latest/reference/generated/networkx.utils.backends._dispatchable.html#dispatchable)). So, `method 4` is not recommended. Instead, mentioning either the full path of the algorithm or the `name` parameter is recommended. For example:

   ```.py
   # using full path
   nx.algorithms.connectivity.connectivity.all_pairs_node_connectivity(H)
   nx.algorithms.approximation.connectivity.all_pairs_node_connectivity(H)

   # using `name` parameter
   nx.all_pairs_node_connectivity(H) # runs the parallel implementation in `connectivity/connectivity`
   nx.approximate_all_pairs_node_connectivity(H) # runs the parallel implementation in `approximation/connectivity`
   ```

2. Right now there isn't much difference between `nx.Graph` and `nxp.ParallelGraph` so `method 3` would work fine but it is not recommended because in future that might not be the case.

Feel free to contribute to nx-parallel. You can find the contributing guidelines [here](https://github.com/networkx/nx-parallel/blob/main/CONTRIBUTING.md). If you'd like to implement a feature or fix a bug, we'd be happy to review a pull request. Please make sure to explain the changes you made in the pull request description. And feel free to open issues for any problems you face, or for new features you'd like to see implemented.

Thank you :)
