# Overview

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance. Refer [NetworkX backends documentation](https://networkx.org/documentation/latest/reference/backends.html) to learn more about the backend architecture in NetworkX.

## Usage

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

You can run your networkx code file with nx-parallel backend by setting an environment variable:

```sh
NETWORKX_BACKEND_PRIORITY="parallel" python nx_code.py
```

Note that for all functions inside `nx_code.py` that are not supported by nx-parallel, will fallback to networkx.

For more, checkout out the [Tutorial notebook](Tutorial.ipynb) on running nx-parallel with free-threaded Python.

### Setting parallel configurations

```py
# Method 1: using NetworkX's config
from ray.util.joblib import register_ray

register_ray()
with nx.config.backends.parallel(backend="ray", n_jobs=5, verbose=10):
    nx.betweenness_centrality(G, backend="parallel")

# Method 2: using Joblib's config
nx.config.backends.parallel.active = False

with joblib.parallel_config(backend="threading", n_jobs=-1, verbose=100):
    nx.betweenness_centrality(G, backend="parallel")
```

For more on how to play with different parallel backends (Loky, Multiprocessing, Threading, Dask, Ray) and configurations in nx-parallel, see [Tutorial](Tutorial.ipynb) and [Config.md](./Config.md). Additionally, refer to the NetworkX's official [backends](https://networkx.org/documentation/latest/reference/backends.html) and [config](https://networkx.org/documentation/latest/reference/configs.html) docs.

---

## Installation

You can install the stable version of nx-parallel using pip:

```sh
pip install nx-parallel
```

or conda:

```sh
conda install nx-parallel
```

For more, see [INSTALL.md](./INSTALL.md).


## A Note on same name functions

Some functions in networkx have the same name but different implementations, so to avoid these name conflicts at the time of dispatching networkx differentiates them by specifying the `name` parameter in the `_dispatchable` decorator of such algorithms. So, `method 3` and `method 4` are not recommended. But, you can use them if you know the correct `name`. For example:

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

---


Feel free to contribute to nx-parallel. You can find the contributing guidelines [here](./CONTRIBUTING.md). If you'd like to implement a feature or fix a bug, we'd be happy to review a pull request. Please make sure to explain the changes you made in the pull request description. And feel free to open issues for any problems you face, or for new features you'd like to see implemented.

This project is managed under the NetworkX organisation, so the [code of conduct of NetworkX](https://github.com/networkx/networkx/blob/main/CODE_OF_CONDUCT.rst) applies here as well.

All code in this repository is available under the Berkeley Software Distribution (BSD) 3-Clause License (see [LICENSE](LICENSE.md)).


Thank you :)
