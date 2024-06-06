# nx-parallel 0.2

We're happy to announce the release of nx-parallel 0.2!

## Enhancements

- parallel implementation for all_pairs_bellman_ford_path ([#14](https://github.com/networkx/nx-parallel/pull/14)).
- benchmarking infrastructure ([#24](https://github.com/networkx/nx-parallel/pull/24)).
- ENH : Adding `backend_info` entry point ([#27](https://github.com/networkx/nx-parallel/pull/27)).
- ENH : added `johnson` in `weighted.py` ([#37](https://github.com/networkx/nx-parallel/pull/37)).
- ENH : added `square_clustering` ([#34](https://github.com/networkx/nx-parallel/pull/34)).
- ENH : improved `all_pairs_bellman_ford_path` ([#49](https://github.com/networkx/nx-parallel/pull/49)).
- ENH : added `node_redundancy` in `bipartite` ([#45](https://github.com/networkx/nx-parallel/pull/45)).
- ENH : adding parallel implementations of `all_pairs_` algos ([#33](https://github.com/networkx/nx-parallel/pull/33)).
- [ENH, BUG] : added `time_tournament_is_strongly_connected` benchmark, renamed `tournament_is_strongly_connected` to `is_strongly_connected` ([#32](https://github.com/networkx/nx-parallel/pull/32)).
- ENH : Added `get_chunks` to `betweenness_centrality` and `create_iterables` in `utils` ([#29](https://github.com/networkx/nx-parallel/pull/29)).

## Bug Fixes

- BUG: moved `get_info` from `backend.py` to `_nx_parallel` ([#53](https://github.com/networkx/nx-parallel/pull/53)).
- BUG : included `_nx_parallel` in packages ([#54](https://github.com/networkx/nx-parallel/pull/54)).

## Documentation

- Update release process ([#21](https://github.com/networkx/nx-parallel/pull/21)).
- DOC: Adding CONTRIBUTING.md, updating readme, etc ([#46](https://github.com/networkx/nx-parallel/pull/46)).

## Maintenance

- replaced **networkx_plugin** with **networkx_backend** ([#25](https://github.com/networkx/nx-parallel/pull/25)).
- replaced networkx.plugins with networkx.backends and updated readme ([#26](https://github.com/networkx/nx-parallel/pull/26)).
- Sync up min python version with networkx main repo ([#31](https://github.com/networkx/nx-parallel/pull/31)).
- MAINT : updated `pre-commit-config.yaml` ([#35](https://github.com/networkx/nx-parallel/pull/35)).
- MAINT : added lint workflow test ([#28](https://github.com/networkx/nx-parallel/pull/28)).
- MAINT : styling fixes ([#38](https://github.com/networkx/nx-parallel/pull/38)).
- MAINT : style fix - 2 ([#40](https://github.com/networkx/nx-parallel/pull/40)).
- MAINT : added `default_benchmark_timeout` to `asv.conf.json` ([#43](https://github.com/networkx/nx-parallel/pull/43)).
- MAINT : removed `NETWORKX_GRAPH_CONVERT` ([#48](https://github.com/networkx/nx-parallel/pull/48)).
- MAINT: updating backend.get_info ([#47](https://github.com/networkx/nx-parallel/pull/47)).
- MAINT: renamed backend function keys ([#50](https://github.com/networkx/nx-parallel/pull/50)).
- MAINT: added script to update `_nx_parallel/__init__.py` ([#57](https://github.com/networkx/nx-parallel/pull/57)).
- MAINT: Renaming functions with a different name while dispatching ([#56](https://github.com/networkx/nx-parallel/pull/56)).
- MAINT: updated `README` and `_nx_parallel/__init__.py` ([#58](https://github.com/networkx/nx-parallel/pull/58)).
- MAINT: Added LICENSE and updated README ([#59](https://github.com/networkx/nx-parallel/pull/59)).
- Use pypi for tests ([#64](https://github.com/networkx/nx-parallel/pull/64)).

## Contributors

4 authors added to this release (alphabetically):

- Aditi Juneja ([@Schefflera-Arboricola](https://github.com/Schefflera-Arboricola))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- Mridul Seth ([@MridulS](https://github.com/MridulS))

5 reviewers added to this release (alphabetically):

- Aditi Juneja ([@Schefflera-Arboricola](https://github.com/Schefflera-Arboricola))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- Mridul Seth ([@MridulS](https://github.com/MridulS))
- Ross Barnowski ([@rossbar](https://github.com/rossbar))

_These lists are automatically generated, and may not be complete or may contain duplicates._

# nx-parallel 0.1

We're happy to announce the release of nx-parallel 0.1!

## Enhancements

- first commit, isolates and betweenness ([#2](https://github.com/networkx/nx-parallel/pull/2)).
- Reconfigure so ParallelGraph stores original nx graph ([#9](https://github.com/networkx/nx-parallel/pull/9)).

## Bug Fixes

- bug fix : changed edge probability from 0.5 to p ([#13](https://github.com/networkx/nx-parallel/pull/13)).

## Documentation

- Update README for Clarity and Comprehension ([#16](https://github.com/networkx/nx-parallel/pull/16)).
- Add release process documentation ([#19](https://github.com/networkx/nx-parallel/pull/19)).

## Maintenance

- add skeleton ([#1](https://github.com/networkx/nx-parallel/pull/1)).
- Add basic test.yaml based on graphblas-algorithms ([#3](https://github.com/networkx/nx-parallel/pull/3)).
- New name for repository ([#8](https://github.com/networkx/nx-parallel/pull/8)).
- Clean up tests, add some minimal docs to readme ([#10](https://github.com/networkx/nx-parallel/pull/10)).
- Use changelist ([#17](https://github.com/networkx/nx-parallel/pull/17)).
- Use hatch as the build backend ([#20](https://github.com/networkx/nx-parallel/pull/20)).
- Use trusted publisher ([#18](https://github.com/networkx/nx-parallel/pull/18)).

## Contributors

6 authors added to this release (alphabetically):

- [@20kavishs](https://github.com/20kavishs)
- Aditi Juneja ([@Schefflera-Arboricola](https://github.com/Schefflera-Arboricola))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- MD ASIFUL ALAM ([@axif0](https://github.com/axif0))
- Mridul Seth ([@MridulS](https://github.com/MridulS))

4 reviewers added to this release (alphabetically):

- Aditi Juneja ([@Schefflera-Arboricola](https://github.com/Schefflera-Arboricola))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- Mridul Seth ([@MridulS](https://github.com/MridulS))

_These lists are automatically generated, and may not be complete or may contain
duplicates._
