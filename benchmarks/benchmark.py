import argparse
import csv
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dataset import generate_arbitrary_routes, generate_monotonic_routes
from src.algorithms import feasible, min_capacity, capacity_lower_bound


def scan_no_pruning(routes, k, capacity):
    ordered = sorted(routes, key=lambda r: (-r.score, r.route_id))
    best = None
    routes_examined = feasibility_checks = capacity_searches = 0
    for r in ordered:
        routes_examined += 1
        feasibility_checks += 1
        if feasible(r.legs, k, capacity):
            capacity_searches += 1
            cap = min_capacity(r.legs, k)
            key = (-r.score, cap, r.route_id)
            if best is None or key < best[0]:
                best = (key, r)
    return best[1] if best else None, routes_examined, feasibility_checks, capacity_searches, 0


def scan_with_pruning(routes, k, capacity):
    ordered = sorted(routes, key=lambda r: (-r.score, r.route_id))
    best = None
    routes_examined = feasibility_checks = capacity_searches = lower_bound_prunes = 0
    for r in ordered:
        routes_examined += 1
        if best is not None and r.score < best[1].score:
            break
        if capacity_lower_bound(r.legs, k) > capacity:
            lower_bound_prunes += 1
            continue
        feasibility_checks += 1
        if feasible(r.legs, k, capacity):
            capacity_searches += 1
            cap = min_capacity(r.legs, k)
            key = (-r.score, cap, r.route_id)
            if best is None or key < best[0]:
                best = (key, r)
    return best[1] if best else None, routes_examined, feasibility_checks, capacity_searches, lower_bound_prunes


def binary_search_routes(routes, k, capacity):
    ordered = sorted(routes, key=lambda r: (r.score, r.route_id))
    lo, hi = 0, len(ordered)
    feasibility_checks = 0
    while lo < hi:
        mid = lo + (hi - lo) // 2
        feasibility_checks += 1
        if feasible(ordered[mid].legs, k, capacity):
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    if idx < 0:
        return None, 0, feasibility_checks, 1, 0
    r = ordered[idx]
    return r, 1, feasibility_checks, 1, 0


def binary_search_capacity(legs, k):
    lo = capacity_lower_bound(legs, k)
    hi = sum(legs)
    checks = 0
    while lo < hi:
        mid = lo + (hi - lo) // 2
        checks += 1
        if feasible(legs, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo, checks


def run_size(size, k, capacity, seed):
    arbitrary = generate_arbitrary_routes(size, seed=seed)
    monotonic = generate_monotonic_routes(size, seed=seed, k=k)

    rows = []

    for name, fn, routes in [
        ("scan_no_pruning", scan_no_pruning, arbitrary),
        ("scan_with_pruning", scan_with_pruning, arbitrary),
        ("binary_search_routes", binary_search_routes, monotonic),
    ]:
        start = time.perf_counter()
        result, examined, checks, cap_searches, prunes = fn(routes, k, capacity)
        elapsed = time.perf_counter() - start
        rows.append({
            "dataset": "arbitrary" if "scan" in name else "monotonic",
            "size": size,
            "algorithm": name,
            "seconds": elapsed,
            "routes_examined": examined,
            "feasibility_checks": checks,
            "capacity_searches": cap_searches,
            "lower_bound_prunes": prunes,
            "result_route_id": result.route_id if result else "",
        })

    route = arbitrary[size // 2]
    start = time.perf_counter()
    cap, checks = binary_search_capacity(route.legs, k)
    elapsed = time.perf_counter() - start
    rows.append({
        "dataset": "single_route",
        "size": len(route.legs),
        "algorithm": "binary_search_capacity",
        "seconds": elapsed,
        "routes_examined": 1,
        "feasibility_checks": checks,
        "capacity_searches": 1,
        "lower_bound_prunes": 0,
        "result_route_id": route.route_id,
    })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[100, 1000, 5000])
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--capacity", type=int, default=300)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", default="results/benchmark_results.csv")
    args = parser.parse_args()

    all_rows = []
    for size in args.sizes:
        all_rows.extend(run_size(size, args.k, args.capacity, args.seed))

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)
    print("Wrote {} benchmark rows to {}".format(len(all_rows), out))


if __name__ == "__main__":
    main()
