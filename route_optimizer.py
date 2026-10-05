"""Algorithmic Route / Score Optimizer."""
from dataclasses import dataclass
from typing import Optional, Sequence

@dataclass(frozen=True)
class Route:
    route_id: str
    score: float
    legs: tuple[int, ...]

    @classmethod
    def from_values(cls, route_id, score, legs):
        legs = tuple(legs)
        if any(x <= 0 for x in legs):
            raise ValueError("All legs must be positive.")
        return cls(route_id, score, legs)

@dataclass(frozen=True)
class RouteResult:
    route_id: str
    score: float
    min_capacity: int

def find_pivot(a: Sequence[float]) -> int:
    """Index of minimum in rotated sorted array; duplicates are safe."""
    if not a:
        raise ValueError("Empty sequence")
    lo, hi = 0, len(a)-1
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] > a[hi]:
            lo = mid+1
        elif a[mid] < a[hi]:
            hi = mid
        else:
            hi -= 1
    return lo

def search_rotated(a: Sequence[float], target: float) -> int:
    """Search target in a rotated sorted array, including duplicates."""
    lo, hi = 0, len(a)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if a[mid] == target:
            return mid
        if a[lo] < a[mid]:
            if a[lo] <= target < a[mid]: hi = mid-1
            else: lo = mid+1
        elif a[lo] > a[mid]:
            if a[mid] < target <= a[hi]: lo = mid+1
            else: hi = mid-1
        else:
            lo += 1
    return -1

def first_score_at_least(rotated_scores, target) -> Optional[int]:
    """First score >= target in logical sorted order; index is original."""
    if not rotated_scores:
        return None
    pivot = find_pivot(rotated_scores)
    n = len(rotated_scores)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo+hi)//2
        if rotated_scores[(pivot+mid)%n] < target:
            lo = mid+1
        else:
            hi = mid
    return None if lo == n else (pivot+lo)%n

def feasible(legs: Sequence[int], k: int, cap: int) -> bool:
    """Greedily test whether legs fit in at most k groups of capacity cap."""
    if k <= 0: return False
    if not legs: return True
    if cap < max(legs): return False
    groups, used = 1, 0
    for d in legs:
        if d > cap: return False
        if used+d > cap:
            groups += 1
            used = d
            if groups > k: return False
        else:
            used += d
    return True

def min_capacity(legs: Sequence[int], k: int) -> int:
    """Binary search the minimum feasible capacity."""
    if not legs: return 0
    if k <= 0: raise ValueError("k must be positive")
    if any(d <= 0 for d in legs):
        raise ValueError("All legs must be positive")
    lo, hi = max(legs), sum(legs)
    while lo < hi:
        mid = (lo+hi)//2
        if feasible(legs, k, mid): hi = mid
        else: lo = mid+1
    return lo

def select_best_routes(routes, min_score, k, capacity_limit=None):
    """Rank qualifying routes by (-score, min_capacity, route_id)."""
    out = []
    for r in routes:
        if r.score < min_score: continue
        cap = min_capacity(r.legs, k)
        if capacity_limit is not None and cap > capacity_limit: continue
        out.append(RouteResult(r.route_id, r.score, cap))
    return sorted(out, key=lambda x: (-x.score, x.min_capacity, x.route_id))

def highest_feasible_score(routes, k, capacity_limit):
    """Return highest score whose route can fit the capacity limit."""
    scores = [r.score for r in routes
              if min_capacity(r.legs, k) <= capacity_limit]
    if not scores: return None
    scores.sort()
    lo, hi = 0, len(scores)
    while lo < hi:
        mid = (lo+hi)//2
        lo = mid+1
    return scores[lo-1]
