# Configuring nx-parallel

In `nx-parallel`, you can control parallel computing settings like `backend`, `n_jobs`, `verbose`, etc. using two configuration systems: `joblib` and `networkx`. Let's break down how to use each of them.

## 1. Using `joblib`

`nx-parallel` relies on `joblib.Parallel` for parallel computing. You can adjust its settings through the `parallel_config` function provided by `joblib`. For more details, check out the official [joblib documentation](https://joblib.readthedocs.io/en/latest/parallel.html).

### 1.1 Usage

```python
from joblib import parallel_config

# Setting global configs
parallel_config(n_jobs=3, verbose=50)
nx.square_clustering(H)

# Setting configs in a context
with parallel_config(n_jobs=7, verbose=0):
    nx.square_clustering(H)
```

## 2. Using `networkx`

To enable networkx's config system in nx-parallel you will need to set the `nx_config` configuration to `True`.

### 2.1 Configs in NetworkX for backends

When you import NetworkX, it sets default configurations for all installed backends, including `nx-parallel`:

```python
import networkx as nx

print(nx.config)
```

Output:

```
NetworkXConfig(backend_priority=[], backends=Config(parallel=ParallelConfig(nx_config=False, backend='loky', n_jobs=None, verbose=0, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})), cache_converted_graphs=True)
```

Setting `nx_config` to `True` tells `nx-parallel` to use NetworkX's configurations instead of `joblib`'s. By default, `nx_config` is set to `False`.

### 2.2 Usage

```python
# enabling networkx's config for nx-parallel
nx.config.backends.parallel.nx_config = True

# Setting global configs
nxp_config = nx.config.backends.parallel
nxp_config.n_jobs = 3
nxp_config.verbose = 50

nx.square_clustering(H)

# Setting config in a context
with nxp_config(n_jobs=7, verbose=0):
    nx.square_clustering(H)
```

The configuration options are the same as `joblib`, so you can refer to the [joblib documentation](https://joblib.readthedocs.io/en/latest/parallel.html) for more details.

### 2.3 How Does NetworkX's Configuration Work in nx-parallel?

In `nx-parallel`, there's a `_set_nx_config` decorator applied to all algorithms. This decorator checks the value of `nx_config`(in `nx.config.backends.parallel`) and then accordingly uses the appropriate configuration system (`joblib` or `networkx`). If `nx_config=True`, it extracts the configs from `nx.config.backends.parallel` and passes them in a `joblib.parallel_config` context manager and calls the function in this context. Otherwise, it simply calls the function.

## 3. Comparing NetworkX and Joblib Configuration Systems

### 3.1 Key Differences

- **Usage**: The main difference is how `backend_params` are passed. In `nx.config` you need to pass them as a dictionary, whereas in `joblib.parallel_config` you can just pass them along with the other configurations.
- **Default Settings**: By default, `nx-parallel` looks for configs set by `joblib.parallel_config`, and NetworkX's config system needs to be enabled explicitly by making the `nx.config.backends.parallel.nx_config` configuration `True`.

### 3.2 When Should You Use Which System?

- Use NetworkX's config system if you're working with multiple backends within NetworkX.
- If you're using `nx-parallel` independently, you can choose either system based on your preference.

## 4. Important Notes

- **What if you use both systems together?** If you try to use both config systems, NetworkX's configuration will take priority, and `joblib`'s settings will be ignored. To avoid this, make sure `networkx.config.backends.parallel.nx_config` is set to `False` when using `joblib` to set configs, and `True` when using `networkx`.
- **Why are there two config systems?** We're working towards syncing both systems in the future so that updating one will automatically update the other. An attempt to move towards a unified configuration system in nx-parallel was made by the PR#68, which introduced a custom context manager for `nx-parallel`.

Feel free to create issues or pull requests if you have any feedback or suggestions to improve this documentation.

Thank you :)
