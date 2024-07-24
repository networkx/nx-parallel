# [WIP] Using Configs

## Current state

All nx-parallel functions implement a `joblib.Parallel` internally, and you change the parameters of that using the `joblib.parallel_config` context manager. We recommend using the `joblib.parallel_config` context manager throughout your code.

Example usage:

```
>>> import networkx as nx
>>> from joblib import parallel_config
>>> from joblib.parallel import get_active_backend
>>> G = nx.complete_graph(4)
>>> get_active_backend()
(<joblib._parallel_backends.LokyBackend object at 0x10348a3c0>, None)
>>> with parallel_config(n_jobs=-1):
... get_active_backend()
... nx.square_clustering(G, backend="parallel")
... with parallel_config(n_jobs=3):
... get_active_backend()
... nx.square_clustering(G, backend="parallel")
... get_active_backend()
...
(<joblib._parallel_backends.LokyBackend object at 0x104a24b30>, -1)
{0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0}
(<joblib._parallel_backends.LokyBackend object at 0x102a99a60>, 3)
{0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0}
(<joblib._parallel_backends.LokyBackend object at 0x10348a3c0>, -1)
>>> get_active_backend()
(<joblib._parallel_backends.LokyBackend object at 0x102a37920>, None)
```

## WIP

- Sync `nx.config.backends.parallel` with default configs in `joblib.parallel_config`, so, something like this is possible. Note that here `nx_parallel_config` is a context manager that behaves almost like `joblib.parallel_config` except that its default configs (only for the outermost config manager) are the configs passed in by the user in the `nx.config.backends.parallel` dataclass.

```py
nx.config.backends.parallel.n_jobs = 3
nx.config.backends.parallel.backend = "loky"
nx.config.backends.parallel.verbose = 15

nx.square_clustering(
    G, backend="parallel"
)  # n_jobs --> 3, backend --> loky, verbose --> 15

with nx_parallel_config(n_jobs=4):
    get_active_backend()
    nx.square_clustering(
        G, backend="parallel"
    )  # n_jobs --> 4, backend --> loky, verbose --> 15
    with nx_parallel_config(verbose=0):
        get_active_backend()
        nx.square_clustering(
            G, backend="parallel"
        )  # n_jobs --> 4, backend --> loky, verbose --> 0
        with nx_parallel_config(n_jobs=5):
            get_active_backend()
            nx.square_clustering(
                G, backend="parallel"
            )  # n_jobs --> 5, backend --> loky, verbose --> 0
        get_active_backend()
    get_active_backend()
get_active_backend()
```

## Notes

- Don't recommend changing global configuration within a context manager, but you can obviously do whatever you want! (Changes made to any global configurations inside a context manager will be lost after exiting that context manager?)

## Resources:

- [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html)
- [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html)
- Using a distributed backend - [docs](https://joblib.readthedocs.io/en/latest/auto_examples/parallel/distributed_backend_simple.html#sphx-glr-auto-examples-parallel-distributed-backend-simple-py)
