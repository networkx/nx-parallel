# Benchmarks

These asv benchmarks are not just good to see how parallel implementations are improving over the commits but you can also compare how much better nx-parallel implementations are as compared to the networkx implementations, by switching the x-axis parameter to be `backends`. There are also heatmaps in the `/timing` folder that show the speedups of the parallel and networkx implementations of the same function.

## Preview benchmarks locally

1. clone this repo and setup the development algorithm(ref. [README](https://github.com/networkx/nx-parallel?tab=readme-ov-file#development-install))
2. run `pip install asv`
3. navigate using `cd benchmarks`
4. If you are working on a different branch then update the value of `branches` in the `asv.conf.json` file.
5. `asv run` will run the benchmarks on the last commit
   - or use `asv continuous base_commit_hash test_commit_hash` to run the benchmark to compare two commits
   - or `asv run -b <benchmark_file_name> -k <benchmark_name>` to run a particular benchmark in a file.
   - or `asv run -b BenchmarkClassName.time_benchmark_func_name` to run a specific benchmark in a benchmark class.
   - if you are running benchmarks for the first time, you will be asked to enter your machine information after this command.
6. `asv publish` will create an `html` folder with the results.
7. `asv preview` will host the results locally at http://127.0.0.1:8080/

<hr>

## Structure of benchmarks

- Each `bench_` file corresponds to a folder/file in the [networkx/algorithms](https://github.com/networkx/networkx/tree/main/networkx/algorithms) directory in NetworkX
- Each class inside a `bench_` file corresponds to every file in a folder(one class if it’s a file) in networkx/algorithms
- The class name corresponds to the file name and the `x` in `bench_x` corresponds to the folder name(class name and `x` are the same if it’s a file in networkx/algorithms)
- Each `time_` function corresponds to each function in the file.
- For other folders in [networkx/networkx](https://github.com/networkx/networkx/tree/main/networkx) like `generators`, `classes`, `linalg`, `utils` etc. we can have different `bench_` files for each of them having different classes corresponding to different files in each of these folders.
- For example: `bench_centrality.py` corresponds to `networkx/algorithms/centrality` folder in NetworkX and the `Betweenness` class inside it corresponds to the `betweenness.py` file in `networkx/algorithms/centrality` folder in NetworkX. And the `time_betweenness_centrality` function corresponds to the `betweenness_centrality` function.
