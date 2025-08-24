# nx-parallel

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance. Refer [NetworkX backends documentation](https://networkx.org/documentation/latest/reference/backends.html) to learn more about the backend architecture in NetworkX.

## Algorithms in nx-parallel

- [adamic_adar_index](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L108)
- [all_pairs_all_shortest_paths](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/generic.py#L11)
- [all_pairs_bellman_ford_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L208)
- [all_pairs_bellman_ford_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L165)
- [all_pairs_dijkstra](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L29)
- [all_pairs_dijkstra_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L122)
- [all_pairs_dijkstra_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L72)
- [all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/connectivity/connectivity.py#L18)
- [all_pairs_shortest_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L62)
- [all_pairs_shortest_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L19)
- [approximate_all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/approximation/connectivity.py#L14)
- [average_clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L213)
- [average_neighbor_degree](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/assortativity/neighbor_degree.py#L10)
- [betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L20)
- [closeness_vitality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/vitality.py#L10)
- [clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L146)
- [cn_soundarajan_hopcroft](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L200)
- [colliders](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/dag.py#L37)
- [common_neighbor_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L158)
- [edge_betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L103)
- [harmonic_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/harmonic.py#L10)
- [is_reachable](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L15)
- [jaccard_coefficient](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L80)
- [johnson](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L251)
- [local_efficiency](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/efficiency_measures.py#L11)
- [node_redundancy](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/bipartite/redundancy.py#L12)
- [number_attracting_components](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/components/attracting.py#L9)
- [number_connected_components](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/components/connected.py#L9)
- [number_of_isolates](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/isolate.py#L9)
- [number_strongly_connected_components](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/components/strongly_connected.py#L9)
- [number_weakly_connected_components](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/components/weakly_connected.py#L9)
- [preferential_attachment](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L133)
- [ra_index_soundarajan_hopcroft](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L232)
- [resource_allocation_index](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L55)
- [square_clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L22)
- [tournament_is_strongly_connected](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L76)
- [triangles](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L84)
- [v_structures](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/dag.py#L13)
- [within_inter_cluster](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/link_prediction.py#L264)

<details>
<summary>Script used to generate the above list</summary>
  
```
import _nx_parallel as nxp
d = nxp.get_funcs_info() # temporarily add `from .update_get_info import *` to _nx_parallel/__init__.py
for func in d:
    print(f"- [{func}]({d[func]['url']})")
```

</details>

## Installation

You can install the stable version of nx-parallel using pip or conda:

```sh
pip install nx-parallel

conda install nx-parallel
```

For more, see [INSTALL.md](./INSTALL.md).

## Usage

You can run your networkx code with nx-parallel backend by:

```sh
export NETWORKX_AUTOMATIC_BACKENDS="parallel" && python nx_code.py
```

Note that for all functions inside `nx_code.py` that do not have an nx-parallel implementation, their original networkx implementation will be executed. You can also use the nx-parallel backend in your code for only some specific function calls in the following ways:

```py
import networkx as nx
import nx_parallel as nxp

G = nx.path_graph(4)
H = nxp.ParallelGraph(G)

# method 1 : passing ParallelGraph object in networkx function (Type-based dispatching)
nx.betweenness_centrality(H)

# method 2 : using the 'backend' kwarg
nx.betweenness_centrality(G, backend="parallel")

# method 3 : using nx-parallel implementation with networkx object
nxp.betweenness_centrality(G)

# method 4 : using nx-parallel implementation with ParallelGraph object
nxp.betweenness_centrality(H)
```

You can also measure the performance gains of parallel algorithms by comparing them to their sequential counter parts. Following is a simple benchmarking setup:

```py
import networkx as nx
import nx_parallel as nxp
from timeit import timeit

G = nx.erdos_renyi_graph(1000, 0.01)
H = nxp.ParallelGraph(G)

sequential = timeit(lambda: nx.betweenness_centrality(G), number=1)
print(f"Sequential: {sequential:.2f}s")

# by default, nx-parallel uses all available cores
parallel = timeit(lambda: nx.betweenness_centrality(H), number=1)
print(f"Parallel:   {parallel:.2f}s")
```

Output:
```sh
Sequential: 1.29s
Parallel:   0.62s
```

### Setting Configurations

You can modify the default NetworkX configurations to control how parallel execution behaves.

Example :

```py
import networkx as nx
import nx_parallel as nxp

G = nx.path_graph(4)

with nx.config.backends.parallel(n_jobs=2, verbose=10):
    nx.betweenness_centrality(G, backend="parallel")
```
For more on how to play with configurations in nx-parallel, see [Config.md](./Config.md). Additionally, refer to the [NetworkX's official backend and config docs](https://networkx.org/documentation/latest/reference/backends.html) for more.

You can also enable logging to observe which backend is used and how tasks are scheduled. Enable and configure logging in the following way:

```py
import logging

nxl = logging.getLogger("networkx")
nxl.addHandler(logging.StreamHandler())
nxl.setLevel(logging.DEBUG)
```

With logging enabled, the example output is as follows:
```sh
Converting input graphs from 'networkx' backend to 'parallel' backend for call to 'betweenness_centrality'
Using backend 'parallel' for call to 'betweenness_centrality' with arguments: (G=<nx_parallel.interface.ParallelGraph object at 0x1027cc5f0>, k=None, normalized=True, weight=None, endpoints=False, seed=<random.Random object at 0x1588a9e20>)
[Parallel(n_jobs=2)]: Using backend LokyBackend with 2 concurrent workers.
[Parallel(n_jobs=2)]: Batch computation too fast (0.16860580444335938s.) Setting batch_size=2.
[Parallel(n_jobs=2)]: Done   2 out of   2 | elapsed:    0.2s finished
```
Refer to [Introspection and Logging section](https://networkx.org/documentation/stable/reference/backends.html#introspection-and-logging) in NetworkX's backend documentation for more.

### Notes

1. Some functions in networkx have the same name but different implementations, so to avoid these name conflicts at the time of dispatching networkx differentiates them by specifying the `name` parameter in the `_dispatchable` decorator of such algorithms. So, `method 3` and `method 4` are not recommended. But, you can use them if you know the correct `name`. For example:

   ```py
   # using `name` parameter - nx-parallel as an independent package

   # run the parallel implementation in `connectivity/connectivity`
   nxp.all_pairs_node_connectivity(H)

   # runs the parallel implementation in `approximation/connectivity`
   nxp.approximate_all_pairs_node_connectivity(H)
   ```

   Also, if you are using nx-parallel as a backend then mentioning the subpackage to which the algorithm belongs is recommended to ensure that networkx dispatches to the correct implementation. For example:

   ```py
   # with subpackage - nx-parallel as a backend
   nx.all_pairs_node_connectivity(H)
   nx.approximation.all_pairs_node_connectivity(H)
   ```

2. Right now there isn't much difference between `nx.Graph` and `nxp.ParallelGraph` so `method 3` would work fine but it is not recommended because in the future that might not be the case.

Feel free to contribute to nx-parallel. You can find the contributing guidelines [here](./CONTRIBUTING.md). If you'd like to implement a feature or fix a bug, we'd be happy to review a pull request. Please make sure to explain the changes you made in the pull request description. And feel free to open issues for any problems you face, or for new features you'd like to see implemented.

This project is managed under the NetworkX organisation, so the [code of conduct of NetworkX](https://github.com/networkx/networkx/blob/main/CODE_OF_CONDUCT.rst) applies here as well.

All code in this repository is available under the Berkeley Software Distribution (BSD) 3-Clause License (see LICENSE).

Thank you :)
