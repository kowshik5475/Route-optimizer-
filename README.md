# Route / Score Optimizer — Python 3.7+ Edition

This project is deliberately written for broad Python compatibility.

## Supported

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13+

It uses only the Python standard library.

## Files

- `route_optimizer.py` — algorithms
- `test_route_optimizer.py` — tests
- `main.py` — command-line demonstration
- `README.md` — documentation

## Run from Windows CMD

```text
cd C:\Users\LAB\Downloads\route_score_optimizer
python main.py
```

Custom run:

```text
python main.py --min-score 80 --legs 3
```

With a capacity limit:

```text
python main.py --min-score 80 --legs 3 --capacity-limit 35
```

## Run tests from CMD

```text
python -m unittest discover -v
```

## Run tests in Jupyter / Colab

Do NOT use plain `unittest.main()`, because notebooks pass their own command-line arguments.

Instead:

```python
from test_route_optimizer import run_tests
run_tests()
```

Or from a notebook cell:

```python
!python -m unittest discover -v
```

## Algorithms

### 1. Rotated-array search

`find_pivot()` finds the smallest value in a rotated sorted array.

With distinct values:

```text
O(log n)
```

With duplicates, the safe `hi -= 1` step means the worst case can become:

```text
O(n)
```

`first_score_at_least()` then performs a binary search in the logical sorted order.

### 2. Minimum capacity

`min_capacity()` searches between:

```text
max(legs)
```

and:

```text
sum(legs)
```

For every candidate capacity, `feasible()` greedily groups consecutive legs.

Because feasibility is monotonic, binary search finds the smallest valid capacity.

For `n` legs and total distance `D`:

```text
O(n log D)
```

### 3. Multiple-route selection

Each route is evaluated with the single-route optimizer.

Results are ordered by:

```text
(-score, min_capacity, route_id)
```

Meaning:

1. Higher score wins.
2. Equal scores use lower capacity.
3. Completely equal results use route ID for deterministic ordering.

## Example output

```text
=== Route / Score Optimizer ===
Minimum score: 80
Maximum legs:  3

Rotated scores: [88, 88, 95, 72, 81]
First score >= threshold: 81

Rank  Route     Score     Min capacity
-----------------------------------------
1     R104      95        30
2     R103      88        28
3     R102      88        35
4     R105      81        30

Winner: R104 (score=95, min_capacity=30)
```
