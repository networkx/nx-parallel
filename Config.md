# Configuring nx-parallel

`nx-parallel` provides flexible parallel computing capabilities, allowing you to control settings like `backend`, `n_jobs`, `verbose`, and more. This can be done through two configuration systems: `joblib` and `NetworkX`. This guide explains how to configure `nx-parallel` using both systems.

## 1. Setting configs using `joblib.parallel_config`

`nx-parallel` relies on [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html) for parallel computing. You can adjust its settings through the [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) class provided by `joblib`. For more details, check out the official [joblib documentation](https://joblib.readthedocs.io/en/latest/parallel.html).

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

Please refer the [official joblib's documentation](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) to better understand the config parameters.

Note: Ensure that `nx.config.backends.parallel.active = False` when using `joblib` for configuration, as NetworkX configurations will override `joblib.parallel_config` settings if `active` is `True`.

## 2. Setting configs using `networkx`'s configuration system for backends

To use NetworkX’s configuration system in `nx-parallel`, you must set the `active` flag (in `nx.config.backends.parallel`) to `True`.

### 2.1 Configs in NetworkX for backends

When you import NetworkX, it automatically sets default configurations for all installed backends, including `nx-parallel`.

```python
import networkx as nx

print(nx.config)
```

Output:

```
NetworkXConfig(
    backend_priority=BackendPriorities(algos=[], generators=[]),
    backends=Config(
        parallel=Config(
            active=False,
            backend="loky",
            n_jobs=None,
            verbose=0,
            temp_folder=None,
            max_nbytes="1M",
            mmap_mode="r",
            prefer=None,
            require=None,
            inner_max_num_threads=None,
            backend_params={},
        )
    ),
    cache_converted_graphs=True,
    fallback_to_nx=False,
    warnings_to_ignore=set(),
)
```

As you can see in the above output, by default, `active` is set to `False`. So, to enable NetworkX configurations for `nx-parallel`, set `active` to `True`. Please refer the [NetworkX's official backend and config docs](https://networkx.org/documentation/latest/reference/backends.html) for more on networkx configuration system.

### 2.2 Usage

```python
# enabling networkx's config for nx-parallel
nx.config.backends.parallel.active = True

# Setting global configs
nxp_config = nx.config.backends.parallel
nxp_config.n_jobs = 3
nxp_config.verbose = 50

nx.square_clustering(H)

# Setting config in a context
with nxp_config(n_jobs=7, verbose=0):
    nx.square_clustering(H)
```

The configuration parameters are the same as `joblib.parallel_config`, so you can refer to the [official joblib's documentation](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) to better understand these config parameters.

### 2.3 How Does NetworkX's Configuration Work in nx-parallel?

In `nx-parallel`, there's a `_configure_if_nx_active` decorator applied to all algorithms. This decorator checks the value of `active`(in `nx.config.backends.parallel`) and then accordingly uses the appropriate configuration system (`joblib` or `networkx`). If `active=True`, it extracts the configs from `nx.config.backends.parallel` and passes them in a `joblib.parallel_config` context manager and calls the function in this context. Otherwise, it simply calls the function.

## 3. Comparing NetworkX and Joblib Configuration Systems

### 3.1 Using Both Systems Simultaneously

You can use both NetworkX’s configuration system and `joblib.parallel_config` together in `nx-parallel`. However, it’s important to understand their interaction.

Example:

```py
# Enable NetworkX configuration
nx.config.backends.parallel.active = True
nx.config.backends.parallel.n_jobs = 6

# Global Joblib configuration
joblib.parallel_config(backend="threading")

with joblib.parallel_config(n_jobs=4, verbose=55):
    # NetworkX config for nx-parallel
    # backend="loky", n_jobs=6, verbose=0
    nx.square_clustering(G, backend="parallel")

    # Joblib config for other parallel tasks
    # backend="threading", n_jobs=4, verbose=55
    joblib.Parallel()(joblib.delayed(sqrt)(i**2) for i in range(10))
```

- **NetworkX Configurations for nx-parallel**: When calling functions within `nx-parallel`, NetworkX’s configurations will override those specified by Joblib. For example, the `nx.square_clustering` function will use the `n_jobs=6` setting from `nx.config.backends.parallel`, regardless of any Joblib settings within the same context.

- **Joblib Configurations for Other Code**: For any other parallel code outside of `nx-parallel`, such as a direct call to `joblib.Parallel`, the configurations specified within the Joblib context will be applied.

This behavior ensures that `nx-parallel` functions consistently use NetworkX’s settings when enabled, while still allowing Joblib configurations to apply to non-NetworkX parallel tasks.

**Key Takeaway**: When both systems are used together, NetworkX's configuration (`nx.config.backends.parallel`) takes precedence for `nx-parallel` functions. To avoid unexpected behavior, ensure that the `active` setting aligns with your intended configuration system.

### 3.2 Key Differences

- **Parameter Handling**: The main difference is how `backend_params` are passed. Since, in networkx configurations are stored as a [`@dataclass`](https://docs.python.org/3/library/dataclasses.html), we need to pass them as a dictionary, whereas in `joblib.parallel_config` you can just pass them along with the other configurations, as shown below:

  ```py
  nx.config.backends.parallel.backend_params = {"max_nbytes": None}
  joblib.parallel_config(backend="loky", max_nbytes=None)
  ```

- **Default Behavior**: By default, `nx-parallel` looks for configs in `joblib.parallel_config` unless `nx.config.backends.parallel.active` is set to `True`.

### 3.3 When Should You Use Which System?

When the only networkx backend you're using is `nx-parallel`, then either of the NetworkX or `joblib` configuration systems can be used, depending on your preference.

But, when working with multiple NetworkX backends, it's crucial to ensure compatibility among the backends to avoid conflicts between different configurations. In such cases, using NetworkX's configuration system to configure `nx-parallel` is recommended. This approach helps maintain consistency across backends. For example:

```python
nx.config.backend_priority = ["another_nx_backend", "parallel"]
nx.config.backends.another_nx_backend.config_1 = "xyz"
joblib.parallel_config(n_jobs=7, verbose=50)

nx.square_clustering(G)
```

In this example, if `another_nx_backend` also internally utilizes `joblib.Parallel` (without exposing it to the user) within its implementation of the `square_clustering` algorithm, then the `nx-parallel` configurations set by `joblib.parallel_config` will influence the internal `joblib.Parallel` used by `another_nx_backend`. To prevent unexpected behavior, it is advisable to configure these settings through the NetworkX configuration system.

**Future Synchronization:** We are working on synchronizing both configuration systems so that changes in one system automatically reflect in the other. This started with [PR#68](https://github.com/networkx/nx-parallel/pull/68), which introduced a unified context manager for `nx-parallel`. For more details on the challenges of creating a compatibility layer to keep both systems in sync, refer to [Issue#76](https://github.com/networkx/nx-parallel/issues/76).

If you have feedback or suggestions, feel free to open an issue or submit a pull request.

Thank you :)
