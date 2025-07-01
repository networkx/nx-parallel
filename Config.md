# Configuring nx-parallel

`nx-parallel` provides flexible parallel computing capabilities, allowing you to control settings like `backend`, `n_jobs`, `verbose`, and more. This can be done through two configuration systems: `joblib` and `NetworkX`. This guide explains how to configure `nx-parallel` using both systems.

## 1. Setting configs using `joblib.parallel_config`

One way to configure `nx-parallel` is by using [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html) for parallel computing. You can adjust its settings through the [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) class provided by `joblib`. For more details, check out the official [joblib documentation](https://joblib.readthedocs.io/en/latest/parallel.html).

### 1.1 Usage

To use [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) with `nx-parallel`, set `nx.config.backends.parallel.active = False`. This disables the default NetworkX configuration so joblib settings can take effect. This can be done globally or within a context manager.

**1.1.1 Disable NetworkX config globally**
```python
from joblib import parallel_config

# Turning off global configs via NetworkX
nx.config.backends.parallel.active = False

# Setting global configs via joblib
parallel_config(n_jobs=5, verbose=50)
nx.square_clustering(H)

# Setting configs within a block of code using a joblib context
with parallel_config(n_jobs=7, verbose=0):
    nx.square_clustering(H)
```

**1.1.2 Disable NetworkX config in a context**
```python
from joblib import parallel_config

# Setting configs in NetworkX's context
with nx.config.backends.parallel(active=False), parallel_config(n_jobs=7, verbose=50):
    nx.square_clustering(H)
```

Please refer to the [official joblib's documentation](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) to better understand the config parameters.

## 2. Setting configs using `networkx`'s configuration system for backends

By default, `nx-parallel` uses NetworkX's configuration system. Please refer to the [NetworkX's official backend and config docs](https://networkx.org/documentation/latest/reference/backends.html) for more on the configuration system.

### 2.1 Configs in NetworkX for backends

When you import NetworkX, it automatically sets default configurations for all installed backends, including `nx-parallel`.

```python
import networkx as nx

print(nx.config)
```

Output:

```
NetworkXConfig(
    backend_priority=BackendPriorities(
        algos=[],
        generators=[]
    ),
    backends=Config(
        parallel=ParallelConfig(
            active=True,
            backend='loky',
            n_jobs=-1,
            verbose=0,
            temp_folder=None,
            max_nbytes='1M',
            mmap_mode='r',
            prefer=None,
            require=None,
            inner_max_num_threads=None,
            backend_params={}
        )
    ),
    cache_converted_graphs=True,
    fallback_to_nx=False,
    warnings_to_ignore=set()
)
```

### 2.2 Usage

```python
# Setting global configs
nxp_config = nx.config.backends.parallel
nxp_config.n_jobs = 3
nxp_config.verbose = 50

nx.square_clustering(H)

# Setting config in a context
with nxp_config(n_jobs=7, verbose=0):
    nx.square_clustering(H)
```

All configuration parameters are the same as `joblib.parallel_config`, so you can refer to the [official joblib's documentation](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html) to better understand these config parameters.

### 2.3 How Does NetworkX's Configuration Work in nx-parallel?

In `nx-parallel`, there's a `_configure_if_nx_active` decorator applied to all algorithms. This decorator checks the value of `active` (in `nx.config.backends.parallel`) and then accordingly uses the appropriate configuration system (`joblib` or `networkx`). Since `active=True` by default, it extracts the configs from `nx.config.backends.parallel` and passes them in a `joblib.parallel_config` context manager and calls the function within this context. If the `active` flag is set to `False`, it simply calls the function.

## 3. Comparing NetworkX and Joblib Configuration Systems

### 3.1 Using Both Systems Simultaneously

You can use both NetworkX’s configuration system and `joblib.parallel_config` together in `nx-parallel`. However, it’s important to understand their interaction.

Example:

```py
# Global NetworkX configuration
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

- **NetworkX Configurations for nx-parallel**: When calling functions within `nx-parallel`, NetworkX’s configurations will override those specified by Joblib because `active` is set to `True` by default. For example, the `nx.square_clustering` function will use the `n_jobs=6` setting from `nx.config.backends.parallel`, regardless of any Joblib settings within the same context.

- **Joblib Configurations for Other Code**: For any other parallel code outside of `nx-parallel`, such as a direct call to `joblib.Parallel`, the configurations specified within the Joblib context will be applied.

This behavior ensures that `nx-parallel` functions consistently use NetworkX’s settings, while still allowing Joblib configurations to apply to non-NetworkX parallel tasks.

To understand using `joblib.parallel_config` within `nx-parallel`, see [the usage guide](#11-usage).

**Key Takeaway**: When both systems are used together, NetworkX's configuration (`nx.config.backends.parallel`) takes precedence for `nx-parallel` functions. To avoid unexpected behavior, ensure that the `active` setting aligns with your intended configuration system.

### 3.2 Key Differences

- **Parameter Handling**: The main difference is how `backend_params` are passed. Since networkx configurations are stored as a [`@dataclass`](https://docs.python.org/3/library/dataclasses.html), we need to pass them as a dictionary, whereas in `joblib.parallel_config` you can just pass them along with the other configurations, as shown below:

  ```py
  nx.config.backends.parallel.backend_params = {"max_nbytes": None}
  joblib.parallel_config(backend="loky", max_nbytes=None)
  ```

- **Default `n_jobs`**: In the NetworkX configuration system, `n_jobs=-1` by default, i.e uses all available CPU cores, whereas `joblib.parallel_config` defaults to `n_jobs=None`. So, parallelism is enabled by default in NetworkX, but must be manually configured when using `joblib.parallel_config`.

    ```python
    # NetworkX
    print(nx.config.backends.parallel.n_jobs)  # Output : -1

    # Joblib
    with joblib.parallel_config() as cfg:
        print(cfg["n_jobs"])  # Output : default(None)
    ```

- **Default Behavior**: By default, `nx-parallel` looks for configs in `nx.config.backends.parallel` unless `active` flag is set to `False`.

### 3.3 When Should You Use Which System?

When the only networkx backend you're using is `nx-parallel`, then either of the NetworkX or `joblib` configuration systems can be used, depending on your preference.

But, when working with multiple NetworkX backends, it's crucial to ensure compatibility among the backends to avoid conflicts between different configurations. In such cases, using NetworkX's configuration system to configure `nx-parallel` is recommended. This approach helps maintain consistency across backends. For example:

```python
nx.config.backend_priority = ["another_nx_backend", "parallel"]
nx.config.backends.another_nx_backend.config_1 = "xyz"
nx.config.backends.parallel.active = False
joblib.parallel_config(n_jobs=7, verbose=50)

nx.square_clustering(G)
```

In this example, if `another_nx_backend` also internally utilizes `joblib.Parallel` (without exposing it to the user) within its implementation of the `square_clustering` algorithm, then the `nx-parallel` configurations set by `joblib.parallel_config` will influence the internal `joblib.Parallel` used by `another_nx_backend`. To prevent unexpected behavior, it is advisable to configure these settings through the NetworkX configuration system.

**Future Synchronization:** We are working on synchronizing both configuration systems so that changes in one system automatically reflect in the other. This started with [PR#68](https://github.com/networkx/nx-parallel/pull/68), which introduced a unified context manager for `nx-parallel`. For more details on the challenges of creating a compatibility layer to keep both systems in sync, refer to [Issue#76](https://github.com/networkx/nx-parallel/issues/76).

If you have feedback or suggestions, feel free to open an issue or submit a pull request.

Thank you :)
