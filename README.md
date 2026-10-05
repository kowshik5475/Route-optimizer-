# Route / Score Optimizer

Code-first project combining:
- duplicate-safe rotated-array binary search;
- binary search on the answer for minimum route capacity;
- greedy feasibility;
- multiple-route selection ranked by `(-score, min_capacity, route_id)`.

## Run
```bash
python main.py
python main.py --min-score 80 --legs 3
python main.py --min-score 80 --legs 3 --capacity-limit 40
```

## Test
```bash
python -m unittest -v
```

## Complexity
For a route with `n` legs and total distance `D`:
- pivot: O(log m) with distinct scores, O(m) worst-case with duplicates;
- rotated lower-bound lookup: O(log m) after pivot;
- greedy feasibility: O(n);
- minimum capacity: O(n log D);
- evaluating `m` routes: O(m*n*log D), assuming comparable route sizes.

The duplicate-safe pivot logic is intentionally explicit because equal values can prevent a normal rotated-array binary search from deciding which half contains the pivot.
