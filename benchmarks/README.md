## Preview benchmarks locally

1. clone this repo
2. `cd benchmarks`
3. `asv run` will run the benchmarks on last commit (or `asv continuous base_commit_hash test_commit_hash` to run the benchmark to compare two commits)
4. `asv publish` will create a `html` folder with the results
5. `asv preview` will host the results locally at http://127.0.0.1:8080/