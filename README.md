# NXParallel

-----------

A NetworkX backend plugin which uses joblib to parallelize graph algorithms.

```python
In [1]: from nx_parallel.interface import Dispatcher; import networkx as nx

In [2]: G = nx.barabasi_albert_graph(1000, 3)

In [3]: d = Dispatcher(nx.betweenness_centrality_subset, backend="dask", processes=4)

In [4]: d(G)

Out[4]: 
{0: 0.1508184529907842,
 1: 0.03628616072632174,
 2: 0.045887560129767795,
 3: 0.0027030059589488193,
 4: 0.17721016416484828,
 5: 0.0557746078502213,
 6: 0.057699260659049456,
 7: 0.03968336805767747,
 8: 0.12732070789945013,
 9: 0.05646396458772636,
 ...
 998: 0.0005573444446765637,
 999: 0.0002854699717699087}
```
