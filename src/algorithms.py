import math
from typing import List, Optional, Sequence, Tuple
from .models import Route, RouteResult


def find_pivot(values: Sequence[float]) -> int:
    if not values:
        raise ValueError("values must be non-empty")
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] < values[hi]:
            hi = mid
        elif values[mid] > values[hi]:
            lo = mid + 1
        else:
            hi -= 1
    return lo


def search_rotated(values: Sequence[float], target: float) -> int:
    if not values:
        return -1
    pivot = find_pivot(values)
    lo, hi = 0, len(values) - 1

    def binary(lo_i: int, hi_i: int) -> int:
        while lo_i <= hi_i:
            mid = lo_i + (hi_i - lo_i) // 2
            if values[mid] == target:
                return mid
            if values[mid] < target:
                lo_i = mid + 1
            else:
                hi_i = mid - 1
        return -1

    if values[pivot] <= target <= values[-1]:
        return binary(pivot, len(values) - 1)
    return binary(0, pivot - 1)


def first_score_at_least(values: Sequence[float], target: float) -> int:
    lo, hi = 0, len(values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo if lo < len(values) else -1


def feasible(legs: Sequence[int], k: int, capacity: int) -> bool:
    if k <= 0:
        raise ValueError("k must be positive")
    if capacity <= 0:
        return False
    if not legs:
        return True
    groups = 1
    current = 0
    for leg in legs:
        if leg > capacity:
            return False
        if current + leg <= capacity:
            current += leg
        else:
            groups += 1
            current = leg
            if groups > k:
                return False
    return True


def capacity_lower_bound(legs: Sequence[int], k: int) -> int:
    if k <= 0:
        raise ValueError("k must be positive")
    if not legs:
        return 0
    return max(max(legs), int(math.ceil(float(sum(legs)) / k)))


def min_capacity(legs: Sequence[int], k: int) -> int:
    if k <= 0:
        raise ValueError("k must be positive")
    if not legs:
        return 0
    lo = capacity_lower_bound(legs, k)
    hi = sum(legs)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(legs, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def _better(candidate: RouteResult, best: Optional[RouteResult]) -> bool:
    if best is None:
        return True
    if candidate.score != best.score:
        return candidate.score > best.score
    if candidate.min_capacity != best.min_capacity:
        return candidate.min_capacity < best.min_capacity
    return candidate.route_id < best.route_id


def best_route_within_capacity(routes: Sequence[Route], k: int, capacity: int) -> Optional[RouteResult]:
    ordered = sorted(routes, key=lambda r: (-r.score, r.route_id))
    best = None
    for route in ordered:
        if best is not None and route.score < best.score:
            break
        if capacity_lower_bound(route.legs, k) > capacity:
            continue
        if not feasible(route.legs, k, capacity):
            continue
        result = RouteResult(route.route_id, route.score, min_capacity(route.legs, k))
        if _better(result, best):
            best = result
    return best


def best_route_monotonic(routes: Sequence[Route], k: int, capacity: int) -> Optional[RouteResult]:
    if not routes:
        return None
    ordered = sorted(routes, key=lambda r: (r.score, r.route_id))
    lo, hi = 0, len(ordered)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(ordered[mid].legs, k, capacity):
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    if idx < 0:
        return None
    route = ordered[idx]
    return RouteResult(route.route_id, route.score, min_capacity(route.legs, k))


def select_best_routes(routes: Sequence[Route], k: int, capacity: Optional[int] = None):
    if capacity is not None:
        return best_route_within_capacity(routes, k, capacity)
    if not routes:
        return None
    best = sorted(routes, key=lambda r: (-r.score, r.route_id))[0]
    return RouteResult(best.route_id, best.score, min_capacity(best.legs, k))
