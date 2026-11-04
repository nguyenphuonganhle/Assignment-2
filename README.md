# Max-flow: Ford-Fulkerson (DFS) vs Edmonds-Karp (BFS)
Primary author of both algorithms: Nguyen Phuong Anh Le
- `maxflow_lib/ford_fulkerson.py`: Ford-Fulkerson, path found by depth-first search
- `maxflow_lib/edmonds_karp.py`: Edmonds-Karp, path found by breadth-first search
## Requirements
Python 3.10 or newer (the reported results used Python 3.14.3 on macOS).
## Build
No compilation is needed. Install the dependencies:
```
python3 -m pip install -r requirements.txt
```
## Run
Run everything (tests, benchmark, analysis, cost-model check):
```
python3 run_all.py
```
Quick check with a reduced set of instances, to confirm the pipeline works:
```
python3 run_all.py --quick
```
Run only the unit tests:
```
python3 -m unittest discover -s tests -t .
```
On Windows, use `python` instead of `python3`. The full run takes several minutes because Ford-Fulkerson is slow on the largest instances.
## Output
Everything is written to `results/`:
- `raw_trials.csv`: every single timing
- `instances.csv`: every input with its counters
- `metadata.json`: Python version and machine
- `summary.md`, `bounds.md`, `outliers.md`, `cost_model.md`, `predictions_vs_measured.md`: tables
- `fig_runtime.png`, `fig_counters.png`, `fig_capacity.png`, `fig_crossover.png`: plots
Every table and figure in the report is generated from these files, and all inputs use fixed seeds, so the numbers can be regenerated.
## Layout
```
maxflow_lib/   network.py, ford_fulkerson.py, edmonds_karp.py, verify.py, generators.py
experiments/   config.py, benchmark.py, analyze.py, bounds.py, outliers.py, cost_model.py
tests/         test_algorithms.py
PREDICTIONS.md
run_all.py
```


