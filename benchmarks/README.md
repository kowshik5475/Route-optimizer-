# Benchmark layer

The benchmark compares four paths:

1. `scan_no_pruning` — baseline fixed-capacity scan.
2. `scan_with_pruning` — fixed-capacity scan with a cheap lower-bound prune.
3. `binary_search_routes` — route-level binary search on deliberately monotonic data.
4. `binary_search_capacity` — binary search on the capacity answer for one route.

The monotonic dataset is constructed so that route capacity requirements are nondecreasing with score. The route-level binary search is only valid under that monotonic feasibility precondition.

Run:

```text
python benchmarks/benchmark.py --sizes 100 1000 5000
python benchmarks/summarize.py
```

Results are written to `results/benchmark_results.csv` and `results/benchmark_summary.csv`.
