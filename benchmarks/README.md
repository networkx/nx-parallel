## Preview benchmarks locally

1. clone this repo
2. `cd benchmarks`
3. `asv run` will run the benchmarks on last commit 
    - or use `asv continuous base_commit_hash test_commit_hash` to run the benchmark to compare two commits
    - or `asv run -b <benchmark_file_name> -k <benchmark_name>` to run a particular benchmark.
    - if you are running benchmarks for the first time, you would be asked to enter your machine information after this command.
4. `asv publish` will create a `html` folder with the results
5. `asv preview` will host the results locally at http://127.0.0.1:8080/