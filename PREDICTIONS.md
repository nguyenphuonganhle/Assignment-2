# Predictions (report section 2). Write these BEFORE you run `python3 run_all.py`. Do not edit them afterwards.

**Honesty note (disclose in your AI-use section).** These predictions were proposed by the AI assistant. They are informed by an earlier,
more complicated exploratory version of this project (random graphs, density, capacity growth) and by one single probe of the matching
crossover (k = 200, seed 0). They are NOT blind predictions. Before you run, read them, change any you disagree with, add 2-3 of your own,
and commit this file. Then your predictions really are made before your results.

Algorithms: Ford-Fulkerson with DFS path choice (FF, Student A) vs Edmonds-Karp with BFS path choice (EK, Student B).
They are the same method (slides 24-25); only the path choice differs.

Theory (slides 42-50):
* FF: at most F = |f*| augmentations, O(F*E). The bound depends on capacity VALUES. A DFS path can be very long and winding.
* EK: at most O(V*E) augmentations, O(V*E^2). The bound does NOT depend on capacity values. Each path has the fewest edges, but each BFS
  explores a whole frontier.
* Cost idea: time grows with (number of augmentations) x (arcs scanned per search). DFS may scan fewer arcs per search, but may need
  more and longer augmentations.

| ID | Prediction | What checks it (experiments/analyze.py) |
|----|------------|-----------------------------------------|
| P1 | Random sparse and random dense graphs (largest size): EK is faster than FF, FF does more augmentations, and FF's average pushed path is at least 2x longer than EK's. | `random_sparse`, `random_dense` |
| P2 | Density sweep (n fixed, edge probability p from 0.03 to 0.9): FF's average path length stays at least 0.3 x n for every p >= 0.12 while EK's stays at most 5, and the FF/EK time ratio is larger at the densest p than at the sparsest. | `density_sweep` |
| P3 | Matching network with unit capacities (largest k): both algorithms do almost the same number of augmentations (within 10%), and FF is faster than EK. | `matching_unit` |
| P4 | Capacity growth on random sparse graphs (same topology, capacities 1..C): FF's augmentations grow at least 10x from C = 1 to C = 10000; EK's grow at most 3x. | `capacity_sweep` |
| P5 | **Crossover.** Matching network with k = 200 and capacities 1..C: FF is faster at C = 1, EK is faster at C = 1000, and the crossover (first C where EK is faster) is somewhere between C = 5 and C = 100. | `matching_crossover` |
| P6 | Counters explain time: on at least 80% of all instances, the sign agrees: if FF scans more arcs than EK in total, it is also slower, and vice versa. | all instances |
