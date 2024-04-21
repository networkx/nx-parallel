# Welcome to nx-parallel!

Hi, Thanks for stopping by!

This project is part of the larger NetworkX project. If you're interested in contributing to nx-parallel, you can first go through the [NetworkX's contributing guide](https://github.com/networkx/networkx/blob/main/CONTRIBUTING.rst) for general guidelines on contributing, setting up the development environment, and adding tests/docs, etc.

## Setting up the development environment

To set the local development environment:

- Fork this repository.
- Clone the forked repository locally.

```.sh
git clone git@github.com:<your_username>/nx-parallel.git
```

- Create a fresh conda/mamba virtualenv ([learn more](https://github.com/networkx/networkx/blob/main/CONTRIBUTING.rst#development-workflow))

```.sh
# Creating a virtual environment
python -m venv nxp-dev

# Activating the venv
source nxp-dev/bin/activate
```

- Install the dependencies using the following command

```.sh
pip install -e ".[developer]"
```

- Install pre-commit actions that will run the linters before making a commit

```.sh
pre-commit install
```

- Create a new branch for your changes using

```.sh
git checkout -b <branch_name>
```

- Stage your changes, run `pre-commit` and then commit and push them and create a PR

```.sh
git add .
pre-commit
git add .
git commit -m "Your commit message"
git push origin <branch_name>
```

## Testing nx-parallel

Firstly, install the dependencies for testing:

```.sh
pip install -e ".[test]"
```

Then run the following command that executes all the tests in networkx's test suite with a `ParallelGraph` object and for algorithms not in nx-parallel, it falls back to networkx's sequential implementations. This is to ensure that the parallel backend follows the same API as networkx's.

```.sh
PYTHONPATH=. \
NETWORKX_TEST_BACKEND=parallel \
NETWORKX_FALLBACK_TO_NX=True \
    pytest --pyargs networkx "$@"
```

Ref. [NetworkX Backend testing docs](https://networkx.org/documentation/latest/reference/backends.html#testing-the-custom-backend) to know about testing mechanisms in networkx.

For running additional tests specific to nx-parallel, you can run the following command:

```.sh
pytest nx_parallel
```

To add any additional tests, **specific to nx_parallel**, you can follow the way test folders are structured in networkx and add your specific test(s) accordingly.

## Documentation syntax

For displaying a small note about nx-parallel's implementation at the end of the main NetworkX documentation, we use the `backend_info` [entry_point](https://packaging.python.org/en/latest/specifications/entry-points/#entry-points) (in the `pyproject.toml` file). The [`get_info` function](https://github.com/networkx/nx-parallel/blob/main/_nx_parallel/__init__.py) is used to parse the docstrings of all the algorithms in nx-parallel and display the nx-parallel specific documentation on the NetworkX's main docs, in the "Additional Backend implementations" box, as shown in the screenshot below.

![backend_box_ss](https://github.com/networkx/nx-parallel/blob/main/assets/images/backend_box_ss.png)

Here is how the docstring should be formatted in nx-parallel:

```.py
def betweenness_centrality(
    G, k=None, normalized=True, weight=None, endpoints=False, seed=None, get_chunks="chunks"
):
"""[FIRST PARA DISPLAYED ON MAIN NETWORKX DOCS AS FUNC DESC]
    The parallel computation is implemented by dividing the
    nodes into chunks and computing betweenness centrality for each chunk concurrently.

    Parameters
    ------------ [EVERYTHING BELOW THIS LINE AND BEFORE THE NETWORKX LINK WILL BE DISPLAYED IN ADDITIONAL PARAMETER'S SECTION ON NETWORKX MAIN DOCS]
    get_chunks : function (default = "chunks")
        A function that takes in nodes as input and returns node_chunks...[YOU CAN MULTIPLE PARAGRAPHS FOR EACH PARAMETER, IF NEEDED, SEPARATED BY 1 BLANK LINE]

    [LEAVE 2 BLANK LINES BETWEEN EACH PARAMETER]
    parameter 2 : int
        ....
    .
    .
    .
    [LEAVE 1 BLANK LINE BETWEEN THE PARAMETERS SECTION AND THE LINK]
    networkx.betweenness_centrality : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html
    """
```

## Chunking

In parallel computing, "chunking" refers to dividing a large task into smaller, more manageable chunks that can be processed simultaneously by multiple computing units, such as CPU cores or distributed computing nodes. It's like breaking down a big task into smaller pieces so that multiple workers can work on different pieces at the same time, and in the case of nx-parallel, this usually speeds up the overall process.

The default chunking in nx-parallel is done by first determining the number of available CPU cores and then allocating the nodes (or edges or any other iterator) per chunk by dividing the total number of nodes by the total CPU cores available. (ref. [chunk.py](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/utils/chunk.py)). This default chunking can be overridden by the user by passing a custom `get_chunks` function to the algorithm as a kwarg. While adding a new algorithm, you can change this default chunking, if necessary (ref. [PR](https://github.com/networkx/nx-parallel/pull/33)). Also, when [the `config` PR](https://github.com/networkx/networkx/pull/7225) is merged in networkx, and the `config` will be added to nx-parallel, then the user would be able to control the number of CPU cores they would want to use and then the chunking would be done accordingly.

## General guidelines on adding a new algorithm

- To get started with adding a new algorithm, you can refer to the existing implementations in nx-parallel and also refer to the [joblib's documentation on embarrassingly parallel `for` loops](https://joblib.readthedocs.io/en/latest/parallel.html).
- The algorithm that you are considering to add to nx-parallel should be in the main networkx repository and it should have the `_dispatchable` decorator. If not, you can consider adding a sequential implementation in networkx first.
- check-list for adding a new function:
  - [ ] Add the parallel implementation(make sure API doesn't break), the file structure should be the same as that in networkx.
  - [ ] add the function to the `Dispatcher` class in [interface.py](https://github.com/networkx/nx-parallel/blob/main/nx_parallel/interface.py) (take care of the `name` parameter in `_dispatchable` (ref. [docs](https://networkx.org/documentation/latest/reference/backends.html)))
  - [ ] update the `__init__.py` files accordingly
  - [ ] docstring following the above format
  - [ ] run the [timing script](https://github.com/networkx/nx-parallel/blob/main/timing/timing_individual_function.py) to get the performance heatmap
  - [ ] add additional test(if any)
  - [ ] add benchmark(s) for the new function(ref. the README in benchmarks folder for more details)

Happy contributing! 🎉
