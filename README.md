# Route/Score Optimizer v3

Python 3.7+ reference implementation for binary-search and resource-capacity experiments.

## Core algorithms

- Duplicate-safe pivot search for rotated sorted arrays.
- Binary search for a score threshold.
- Greedy capacity feasibility.
- Binary search for minimum required capacity.
- Fixed-capacity best-route selection with deterministic tie-breaking.
- Route-level binary search only when score-to-feasibility is monotonic.

## Complexity

- One route minimum capacity: `O(n log D)`, where `D` is total leg distance.
- Arbitrary routes with fixed capacity: worst-case `O(mn)` for `m` routes and `n` legs per route; lower-bound pruning improves practical work.
- Monotonic routes with fixed capacity: about `O(n log m)` for comparable route sizes.

Duplicate values in rotated arrays can make pivot search `O(n)` in the worst case because equal endpoints may need to be discarded.

## Tests

```text
python -m unittest discover -v
```

## Dataset generation

```text
python generate_dataset.py --routes 10000 --type arbitrary --output datasets/arbitrary_10000.csv
python generate_dataset.py --routes 10000 --type monotonic --output datasets/monotonic_10000.csv
```

## Benchmarks

```text
python benchmarks/benchmark.py --sizes 100 1000 5000
python benchmarks/summarize.py
```

The benchmark records execution time, routes examined, feasibility checks, capacity searches, and lower-bound prunes.
