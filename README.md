# nx-parallel

nx-parallel is a NetworkX backend that uses joblib for parallelization. This project aims to provide parallelized implementations of various NetworkX functions to improve performance.

## Algorithms in nx-parallel

- [betweenness_centrality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/betweenness.py#15)
- [square_clustering](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/cluster.py#10)
- [local_efficiency](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/efficiency_measures.py#9)
- [number_of_isolates](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/isolate.py#8)
- [is_reachable](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#10)
- [tournament_is_strongly_connected](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/tournament.py#54)
- [closeness_vitality](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/vitality.py#9)
- [all_pairs_bellman_ford_path](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/weighted.py#16)
- [johnson](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/algorithms/weighted.py#59)

<details>
<summary>Script used to generate the above list</summary>
  
```.py
import nx_parallel as nxp
d = nxp.get_info()
for func in d.get("functions", {}):
    print(f"- [{func}]({d['functions'][func]['url']})")
```

</details>

## Backend usage

```.py
import networkx as nx
import nx_parallel as nxp

G = nx.path_graph(4)
H = nxp.ParallelGraph(G)

# method 1 : passing ParallelGraph object in networkx function
nx.betweenness_centrality(H)

# method 2 : using the 'backend' kwarg
nx.betweenness_centrality(G, backend="parallel")


# Not recommended but possible

# method 3 : using nx-parallel implementation with networkx object
nxp.betweenness_centrality(G)

# method 4 : using nx-parallel implementation with ParallelGraph object
nxp.betweenness_centrality(H)

# output : {0: 0.0, 1: 0.6666666666666666, 2: 0.6666666666666666, 3: 0.0}
```

Feel free the contribute to nx-parallel. You can find the contributing guidelines [here](https://github.com/networkx/nx-parallel/blob/main/CONTRIBUTING.md). If you'd like to implement a feature or fix a bug, we'd be happy to review a pull request. Please make sure to explain the changes you made in the pull request description. And feel free to open issues for any problems you face, or for new features you'd like to see implemented.

Thank you :)
