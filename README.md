# nx-parallel

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance. Refer [NetworkX backends documentation](https://networkx.org/documentation/latest/reference/backends.html) to learn more about the backend architecture in NetworkX.

## Algorithms in nx-parallel

- [all_pairs_all_shortest_paths](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/generic.py#L11)
- [all_pairs_bellman_ford_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L212)
- [all_pairs_bellman_ford_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L168)
- [all_pairs_dijkstra](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L29)
- [all_pairs_dijkstra_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L124)
- [all_pairs_dijkstra_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L73)
- [all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/connectivity/connectivity.py#L18)
- [all_pairs_shortest_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L63)
- [all_pairs_shortest_path_length](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/unweighted.py#L19)
- [approximate_all_pairs_node_connectivity](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/approximation/connectivity.py#L13)
- [betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L20)
- [closeness_vitality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/vitality.py#L10)
- [edge_betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/centrality/betweenness.py#L96)
- [is_reachable](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L13)
- [johnson](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/shortest_paths/weighted.py#L256)
- [local_efficiency](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/efficiency_measures.py#L10)
- [node_redundancy](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/bipartite/redundancy.py#L12)
- [number_of_isolates](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/isolate.py#L9)
- [square_clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#L11)
- [tournament_is_strongly_connected](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#L59)

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

It is recommended to first refer the [NetworkX's INSTALL.rst](https://github.com/networkx/networkx/blob/main/INSTALL.rst).
nx-parallel requires Python >=3.11. Right now, the only dependencies of nx-parallel are networkx and joblib.

### Installing nx-parallel using `pip`

You can install the stable version of nx-parallel using pip:

```sh
pip install nx-parallel
```

The above command also installs the two main dependencies of nx-parallel i.e. networkx
and joblib. To upgrade to a newer release use the `--upgrade` flag:

```sh
pip install --upgrade nx-parallel
```

### Installing the development version

Before installing the development version, you may need to uninstall the
standard version of `nx-parallel` and other two dependencies using `pip`:

```sh
pip uninstall nx-parallel networkx joblib
```

Then do:

```sh
pip install git+https://github.com/networkx/nx-parallel.git@main
```

### Installing nx-parallel with conda

Installing `nx-parallel` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

```sh
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Once the `conda-forge` channel has been enabled, `nx-parallel` can be installed with `conda`:

```sh
conda install nx-parallel
```

or with `mamba`:

```sh
mamba install nx-parallel
```

## Backend usage

You can run your networkx code by just setting the `NETWORKX_AUTOMATIC_BACKENDS` environment variable to `parallel`:

```sh
export NETWORKX_AUTOMATIC_BACKENDS=parallel && python nx_code.py
```

Note that for all functions inside `nx_code.py` that do not have an nx-parallel implementation their original networkx implementation will be executed. You can also use the nx-parallel backend in your code for only some specific function calls in the following ways:

```py
import networkx as nx
import nx_parallel as nxp

# enabling networkx's config for nx-parallel
nx.config.backends.parallel.active = True

# setting `n_jobs` (by default, `n_jobs=None`)
nx.config.backends.parallel.n_jobs = 4

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

For more on how to play with configurations in nx-parallel refer the [Config.md](./Config.md)! Additionally, refer the [NetworkX's official backend and config docs](https://networkx.org/documentation/latest/reference/backends.html) for more on functionalities provided by networkx for backends and configs like logging, `backend_priority`, etc. Another way to configure nx-parallel is by using [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html).

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
