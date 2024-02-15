# Welcome to nx-parallel

Hi! Thanks for stopping by!

This project is part of the larger NetworkX project. If you're interested in contributing to NetworkX, please first go through the [NetworkX contributing guidelines](https://github.com/networkx/networkx/blob/main/CONTRIBUTING.rst) for general guidelines on contributing, setting up the development environment, and adding tests/docs, etc.

- **Issues:** Feel free to open issues for any problems you face, or for new features you'd like to see implemented.
- **Pull requests:** If you'd like to implement a feature or fix a bug yourself, we'd be happy to review a pull request. Please make sure to explain the changes you made in the pull request description.

## To setup a local development environment

- Fork this repository.
- Clone the forked repository locally.

```
git clone git@github.com:<your_username>/networkx.git
```

- Create a fresh conda/mamba virtualenv and install the dependencies

```
pip install -e ".[developer]"
```

- Install pre-commit actions that will run the linters before making a commit

```
pre-commit install
```

## Testing

The following command runs all the tests in networkx with a `ParallelGraph` object and for algorithms not in nx-parallel, it falls back to networkx's implementation. This is to ensure that the parallel implementation follows the same API as networkx's.

```
PYTHONPATH=. \
NETWORKX_GRAPH_CONVERT=parallel \
NETWORKX_TEST_BACKEND=parallel \
NETWORKX_FALLBACK_TO_NX=True \
    pytest --pyargs networkx "$@"
```

For running additional tests:

```
pytest nx_parallel
```

To add any additional tests, **specific to nx_parallel**, you can follow the way tests folders are structured in networkx and add your specific test(s) accordingly.

## Documentation syntax

The docstring of functions should be as follows, e.g. :

```.py
def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None
):
"""[FIRST PARA DISPLAYED ON MAIN NETWORKX DOCS AS FUNC DESC]
    The parallel computation is implemented by dividing the
    nodes into chunks and computing betweenness centrality for each chunk concurrently.
    
    Parameters 
    ------------ [EVERYTHING BELOW THIS LINE AND BEFORE THE NETWORKX LINK WILL BE DISPLAYED IN ADDITIONAL PARAMETER'S SECTION ON NETWORKX MAIN DOCS]
    get_chunks : function (default = None)
         A function that takes in nodes as input and returns node_chuncks
    parameter 2 : int
        desc ....
    .
    .
    .

    networkx.betweenness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html
    """

```

## To Chunk or not to Chunk(update)

In the nx-parallel, the nodes are divided into chunks and the computation is done concurrently. The decision to chunk the nodes or not is based on the algorithm. For example, if the overhead of chunking and managing the chunks might be more than the actual computation then in such cases it is better to run the algorithm parallelly on nodes(edges, paths, etc.) instead of node_chunks(edge_chunks, path_chunks etc).

- if you are not sure whether to chunk the nodes or not, you can add a parameter `get_chunks` to the function, a user-defined function that takes in nodes as input and returns node_chuncks. This way, the user can provide a custom function to chunk the nodes based on the graph and the algorithm.
- you can choose to not allow chunking at all by adding the `is_chunk` parameter to the function. This way, the user can decide if they want to use chunking or not.
- you can also try benchmarking the chunk and no_chunk versions of your algorithm to make a decision(ref. [PR 42](https://github.com/networkx/nx-parallel/pull/42)).
- if there is a lot of processing after the parallel part is implemented, it might be better to have chunks in that case(but it depends on the post-processing of chunks).

## General guidelines on adding a new algorithm

- The algorithm you are considering adding should preferably be a parallel version of an existing algorithm in networkx. If not, you can consider adding a sequential implementation in networkx first.
- check-list for adding a new function:
  - [ ] Add the parallel implementation(make sure API doesn't break), the file structure is the same as that of networkx's.
  - [ ] docstring following the above format
  - [ ] additional test(if any)
  - [ ] add the function in interface.py
  - [ ] update the `__init__.py` files accordingly
  - [ ] add benchmark(s) for the new function(ref the README in benchmarks folder for more details on how the benchmarks are structured)
  - [ ] run the timing script to get the performance heatmap
  - [ ] add the function to the README.md under the features section


Happy contributing! 🎉
