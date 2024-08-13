# Using Configurations in nx-parallel

nx-parallel algorithms internally use the [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) context manager. You can change the configuration parameters of this internal `joblib.parallel_config` context manager using [NetworkX's config](https://networkx.org/documentation/latest/reference/backends.html#module-networkx.utils.configs) context manager. The internal `joblib.parallel_config` context manager uses the [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html) call, which is responsible for all the parallel process creation.

## Default Configuration

When you import NetworkX, the default configurations for all the installed backends are set as shown below:

```python
import networkx as nx

nx.config
```

Output:

```
NetworkXConfig(backend_priority=[], backends=Config(parallel=ParallelConfig(backend='loky', n_jobs=None, verbose=0, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})), cache_converted_graphs=True)
```

### Note

The default settings of `joblib.parallel_config` are the same as the default configs in the `ParallelConfig` class, except for the `backend` config, which is `None` in `joblib.parallel_config` and `"loky"` in `ParallelConfig`. This prevents errors when using the NetworkX config, as the internal `joblib.Parallel`'s `backend` default is `"loky"` when not specified. This consistency in user experience is maintained for ease of use. Additinally, by default the `n_jobs` value is `-1`.

## Modifying Configuration

The `ParallelConfig` class inherits from NetworkX's `Config` class. You can use this as a `dataclass` or as a context manager to change the nx-parallel configurations.

### As a config variable

You can directly set the desired parameters:

```python
nxp_config = nx.config.backends.parallel
nxp_config.n_jobs = 6
nxp_config.verbose = 15

G = nx.complete_graph(20)

# backend -> loky, n_jobs -> 6, verbose -> 15
nx.square_clustering(G, backend="parallel")
```

### As a Context Manager

You can use the context manager to temporarily change configuration parameters for specific code blocks:

```python
# in continuation with the above code block

with nxp_config(n_jobs=4):
    # backend -> loky, n_jobs -> 4, verbose -> 15
    nx.square_clustering(G, backend="parallel")
    with nxp_config(backend="threading", verbose=0):
        # backend -> threading, n_jobs -> 4, verbose -> 0
        nx.betweenness_centrality(G, backend="parallel")
        with nxp_config(n_jobs=8):
            # backend -> threading, n_jobs -> 8, verbose -> 0
            nx.number_of_isolates(G, backend="parallel")
```

From the comments, you can observe how the context managers acquire the configurations from the outer context manager or the global configurations when the context manager is not inside any context manager.

Note that using `joblib.parallel_config` will output unexpected results. We recommend using the NetworkX's config context manager, as it is the same as the `joblib.parallel_config` context manager because it only provides the configurations to the internal `joblib.parallel_config` context manager.

Also, modifying the global config inside a context manager will update the configuration inside as well as outside the context manager permanently, as shown below:

```python
nxp_config.n_jobs = 6

nx.square_clustering(G, backend="parallel")  # n_jobs -> 6

with nxp_config(n_jobs=4):
    nx.square_clustering(G, backend="parallel")  # n_jobs -> 4
    nxp_config.n_jobs = 8
    nx.square_clustering(G, backend="parallel")  # n_jobs -> 8

nx.square_clustering(G, backend="parallel")  # n_jobs -> 8
```

Please feel free to create issues or PRs if you want to improve this documentation or if you have any feedback.

Thank you :)
