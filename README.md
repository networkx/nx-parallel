NX-Parallel
-----------

A NetworkX backend plugin which uses dask for parallelization.

``` python
In [1]: import networkx as nx; import nx_parallel

In [2]: G = nx.erdos_renyi_graph(10, 0.5)

In [3]: H = nx_parallel.ParallelGraph(G)

In [4]: nx.betweenness_centrality(H)
Out[4]: 
{0: 0.0,
 1: 0.0,
 2: 0.0,
 3: 0.0,
 4: 0.0,
 5: 0.0,
 6: 0.0,
 7: 0.0,
 8: 0.0,
 9: 0.0}

```