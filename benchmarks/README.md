## Preview benchmarks locally

1. clone this repo
2. `cd benchmarks`
3. If you are working on a different branch then update the `branches` in the `asv.conf.json` file.
4. `asv run` will run the benchmarks on the last commit
   - or use `asv continuous base_commit_hash test_commit_hash` to run the benchmark to compare two commits
   - or `asv run -b <benchmark_file_name> -k <benchmark_name>` to run a particular benchmark.
   - if you are running benchmarks for the first time, you will be asked to enter your machine information after this command.
5. `asv publish` will create a `html` folder with the results
6. `asv preview` will host the results locally at http://127.0.0.1:8080/

<hr>

## Structure of benchmarks

- Each `bench_` file corresponds to a folder/file in the [networkx/algorithms](https://github.com/networkx/networkx/tree/main/networkx/algorithms) directory in NetworkX
- Each class inside a `bench_` file corresponds to every file in a folder(one class if it’s a file) in networkx/algorithms
- The class name corresponds to the file name and the `x` in `bench_x` corresponds to the folder name(class name and `x` are the same if it’s a file in networkx/algorithms)
- Each `time_` function corresponds to each function in the file.
- For other folders in [networkx/networkx](https://github.com/networkx/networkx/tree/main/networkx) like `generators`, `classes`, `linalg`, `utils` etc. we can have different `bench_` files for each of them having different classes corresponding to different files in each of these folders.
- For example: `bench_centrality.py` corresponds to `networkx/algorithms/centrality` folder in NetworkX and the `Betweenness` class inside it corresponds to the `betweenness.py` file in `networkx/algorithms/centrality` folder in NetworkX. And the `time_betweenness_centrality` function corresponds to the `betweenness_centrality` function.
