# Max-flow: Ford–Fulkerson (DFS) vs Edmonds–Karp (BFS)   (Theme 3: theoretical-optimal vs practical)

| Algorithm | File | Primary author |
|---|---|---|
| Ford–Fulkerson, path found by depth-first search | `maxflow_lib/ford_fulkerson.py` | **Student A** (put your real name) |
| Edmonds–Karp, path found by breadth-first search | `maxflow_lib/edmonds_karp.py` | **Student B** (put your real name) |

Both are the same Week 8 method (slides 24–25: "it does not specify which augmenting path to choose"). Only the path choice differs.
Question: Ford–Fulkerson's bound O(F·E) depends on the capacity values, Edmonds–Karp's O(V·E²) does not. **Where does that
difference show up in practice, and where does the simpler DFS actually win?** The matching experiment finds the crossover.

## How to run (Mac / Linux / Windows, Python 3.10 or newer)
```
python3 -m pip install -r requirements.txt
python3 run_all.py            # tests, then benchmark (checks every answer first), then tables/plots/prediction checks (about 6-10 min)
python3 run_all.py --quick    # short smoke test (about 2 min); do not use its numbers in the report
```
On Windows use `python` instead of `python3`. To run only the tests: `python3 -m unittest discover -s tests -t .`

Everything is written to `results/`: `raw_trials.csv` (every single timing), `instances.csv` (every input with its counters),
`metadata.json` (Python version, machine), `summary.md` (tables), `predictions_vs_measured.md`, `fig_*.png`.
Every table and plot is produced by `experiments/analyze.py` from those files, so every number in the report can be regenerated.

## Files
```
maxflow_lib/   network.py (residual graph)   ford_fulkerson.py   edmonds_karp.py   verify.py (answer checks)   generators.py (inputs)
experiments/   config.py (all inputs and sizes)   benchmark.py (timing harness)   analyze.py (tables, plots, prediction checks)
tests/         test_algorithms.py
PREDICTIONS.md   write your predictions here BEFORE you run
run_all.py       one command for everything
```

## What the experiments are
| Family | What it varies | Why |
|---|---|---|
| `random_sparse`, `random_dense` | graph size | basic comparison |
| `density_sweep` | edge probability, size fixed | does the DFS find the sink faster in dense graphs? |
| `matching_unit` | size, all capacities 1 (slide 56 network) | where all augmentations carry one unit |
| `capacity_sweep` | largest capacity C, same graph shape | do capacity values matter in practice? |
| `matching_crossover` | C = 1 … 1000 on the matching network | **finds the crossover** between the two algorithms |

Counters recorded for every run: paths pushed (augmentations), arcs scanned, total path length. They are used to *explain* the timings.

## How the answers are checked (methodology)
* Before any timing, every instance is solved by both algorithms and each answer is checked: capacity and conservation hold (slides 5–6) and a cut
  with exactly the same capacity exists (slide 32, max-flow = min-cut). The two flow values must be equal.
* Generating an input is never timed. One untimed warm-up run, then 5 timed runs per algorithm, alternating which goes first, garbage collector off.
* Every timing is saved. Plots show the median and the minimum-to-maximum range over all seeds and repetitions. Seeds are fixed, so inputs repeat.
* Timings are pure Python, so they measure the interpreter as well as the algorithm; the operation counters do not depend on the machine.

## Week 8 slide map
| Slide idea | Where |
|---|---|
| st-flow, capacity and conservation (5–6) | `verify.check_flow` |
| greedy gets stuck at 18, maximum is 21 (14–17) | `test_greedy_gets_stuck_at_18_but_the_maximum_is_21` |
| residual network, backward edges (18–20) | `network.py`: arc `e` and its reverse `e ^ 1`; `test_reverse_edge_is_required` |
| Ford–Fulkerson method (24–25), O(F·E) (41–43) | `ford_fulkerson.py`; `test_ford_fulkerson_needs_at_most_F_augmentations` |
| cuts, weak duality (26–31) | `verify.cut_capacity`; `test_weak_duality_...` |
| max-flow = min-cut, cut from the reachable set (32–40, Q1 on 53) | `verify.min_cut_source_side`; `test_min_cut_is_read_off_the_residual_network` |
| irrational capacities may not terminate (44) | capacities must be integers (`test_bad_input_is_rejected`) |
| a bad path choice forces many augmentations (46) | `test_diamond_needs_2M_augmentations_if_the_paths_alternate`; `capacity_sweep` |
| Edmonds–Karp, O(V·E) augmentations (45–50) | `edmonds_karp.py`; `test_edmonds_karp_needs_at_most_V_times_E_augmentations` |
| matching as flow, Kőnig (55–66) | `generators.bipartite`; `test_matching_flow_equals_matching_equals_vertex_cover` |
| matrix rounding (71–74) | `test_matrix_rounding_puzzle` |
