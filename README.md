## nx-parallel

A NetworkX backend plugin which uses joblib and multiprocessing for parallelization.

```python
In [1]: import networkx as nx; import nx_parallel

In [2]: G = nx.path_graph(4)

In [3]: H = nx_parallel.ParallelGraph(G)

In [4]: nx.betweenness_centrality(H)
Out[4]: {0: 0.0, 1: 0.6666666666666666, 2: 0.6666666666666666, 3: 0.0}

```

Currently the following functions have parallelized implementations:

```
├── centrality
│   ├── betweenness_centrality
│   ├── closeness_vitality
├── tournament
│   ├── is_reachable
├── efficiency_measures
│   ├── local_efficiency
```

![alt text](timing/heatmap_all_functions.png)

See the `/timing` folder for more heatmaps and code for heatmap generation!


### Development install

To setup a local development:

- Fork this repository.
- Clone the forked repository locally.
```
$ git clone git@github.com:<your_username>/networkx.git
```
- Create a fresh conda/mamba virtualenv and install the dependencies
```
$ pip install -e ".[developer]"
```
- Install pre-commit actions that will run the linters before making a commit
```
$ pre-commit install
```
- Make sure you can run the tests locally with
```
PYTHONPATH=. \
NETWORKX_GRAPH_CONVERT=parallel \
NETWORKX_TEST_BACKEND=parallel \
NETWORKX_FALLBACK_TO_NX=True \
    pytest --pyargs networkx "$@"
```