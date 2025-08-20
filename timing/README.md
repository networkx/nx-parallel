# Timing Comparisons

Compares the performance of nx-parallel and NetworkX algorithms with the help of heatmaps.

The `timing/` folder has two subfolders, each with a `timing_individual_function.py` and its corresponding heatmaps:  

- `new_heatmaps/` → new timing script + heatmaps  
- `old_heatmaps/` → old timing script + heatmaps

## Machine Specifications

### Machine used for new heatmaps

Model: 14-inch MacBook Pro (2024)

CPU: Apple M4

RAM: 16 GB unified Memory

### Machine used for old heatmaps

Model: 13-inch MacBook Pro (2020)

CPU: 2 GHz Quad-Core Intel Core i5

RAM: 16 GB LPDDR4X at 3733 MHz

## Heatmaps

### New Heatmaps (`new_heatmaps/`)

betweeness_centrality
![alt text](new_heatmaps/heatmap_betweenness_centrality_timing.png)

edge_betweeness_centrality
![alt text](new_heatmaps/heatmap_edge_betweenness_centrality_timing.png)

number_of_isolates
![alt text](new_heatmaps/heatmap_number_of_isolates_timing.png)

tournament.is_reachable
![alt text](new_heatmaps/heatmap_is_reachable_timing.png)

node_redundancy
![alt text](new_heatmaps/heatmap_node_redundancy_timing.png)

## Old heatmaps (`old_heatmaps/`):

all_pairs_all_shortest_paths
![alt text](old_heatmaps/heatmap_all_pairs_all_shortest_paths_timing.png)

all_pairs_bellman_ford_path
![alt text](old_heatmaps/heatmap_all_pairs_bellman_ford_path_timing.png)

all_pairs_bellman_ford_path_length
![alt text](old_heatmaps/heatmap_all_pairs_bellman_ford_path_length_timing.png)

all_pairs_dijkstra_path
![alt text](old_heatmaps/heatmap_all_pairs_dijkstra_path_timing.png)

all_pairs_dijkstra_path_length
![alt text](old_heatmaps/heatmap_all_pairs_dijkstra_path_length_timing.png)

all_pairs_node_connectivity
![alt text](old_heatmaps/heatmap_all_pairs_node_connectivity_timing.png)

all_pairs_shortest_path
![alt text](old_heatmaps/heatmap_all_pairs_shortest_path_timing.png)

all_pairs_shortest_path_length
![alt text](old_heatmaps/heatmap_all_pairs_shortest_path_length_timing.png)

closeness_vitality
![alt text](old_heatmaps/heatmap_closeness_vitality_timing.png)

is_strongly_connected
![alt text](old_heatmaps/heatmap_is_strongly_connected_timing.png)

johnson
![alt text](old_heatmaps/heatmap_johnson_timing.png)

local_efficiency
![alt text](old_heatmaps/heatmap_local_efficiency_timing.png)

square_clustering
![alt text](old_heatmaps/heatmap_square_clustering_timing.png)

