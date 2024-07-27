# Using Configs

nx-parallel algorithms have a `joblib.parallel_config` context manager which has the `joblib.Parallel` instance. You change the config parameters of the internal `joblib.parallel_config` context manager using networkx's context manager, like this:

```
>>> import networkx as nx
>>> nx.config # default configs
NetworkXConfig(backend_priority=[], backends=Config(parallel=ParallelConfig(backend=None, n_jobs=None, verbose=0, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})), cache_converted_graphs=True)
>>>
>>> nxp_config = nx.config.backends.parallel
>>> nxp_config.backend = "loky" # global config
>>>
>>> G = nx.complete_graph(20)
>>> # using context manager
>>> with nxp_config(n_jobs=4): # backend -> loky , n_jobs -> 4 , verbose -> 0
...     nx.square_clustering(G, backend="parallel")
...     nxp_config
...     print()
...     with nxp_config(n_jobs=3, verbose=15): # backend -> loky , n_jobs -> 3 , verbose -> 15
...         nx.square_clustering(G, backend="parallel")
...         nxp_config
...         print()
...         with nxp_config(verbose=0): # backend -> loky , n_jobs -> 3 , verbose -> 0
...             nx.square_clustering(G, backend="parallel")
...             nxp_config
...
{0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0, 16: 1.0, 17: 1.0, 18: 1.0, 19: 1.0}
ParallelConfig(backend='loky', n_jobs=4, verbose=0, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})

[Parallel(n_jobs=3)]: Using backend LokyBackend with 3 concurrent workers.
[Parallel(n_jobs=3)]: Done   1 tasks      | elapsed:    0.1s
[Parallel(n_jobs=3)]: Batch computation too fast (0.09458684921264648s.) Setting batch_size=2.
[Parallel(n_jobs=3)]: Done   2 out of   4 | elapsed:    0.1s remaining:    0.1s
[Parallel(n_jobs=3)]: Done   4 out of   4 | elapsed:    0.1s finished
{0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0, 16: 1.0, 17: 1.0, 18: 1.0, 19: 1.0}
ParallelConfig(backend='loky', n_jobs=3, verbose=15, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})

{0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0, 16: 1.0, 17: 1.0, 18: 1.0, 19: 1.0}
ParallelConfig(backend='loky', n_jobs=3, verbose=0, temp_folder=None, max_nbytes='1M', mmap_mode='r', prefer=None, require=None, inner_max_num_threads=None, backend_params={})
>>>
```

## Resources

- [NetworkX's Config docs](https://networkx.org/documentation/latest/reference/backends.html#module-networkx.utils.configs)
- [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html)
- [`joblib.parallel_config`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_config.html)
- Using a distributed backends - [docs](https://joblib.readthedocs.io/en/latest/auto_examples/parallel/distributed_backend_simple.html#sphx-glr-auto-examples-parallel-distributed-backend-simple-py)
