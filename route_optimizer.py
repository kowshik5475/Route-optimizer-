"""
Route / Score Optimizer
Compatible with Python 3.7+.
Standard library only.
"""

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple, List


@dataclass(frozen=True)
class Route:
    route_id: str
    score: float
    legs: Tuple[int, ...]

    @classmethod
    def from_values(cls, route_id, score, legs):
        legs = tuple(legs)
        if any(x <= 0 for x in legs):
            raise ValueError("All route legs must be positive.")
        return cls(route_id, score, legs)


@dataclass(frozen=True)
class RouteResult:
    route_id: str
    score: float
    min_capacity: int


def find_pivot(a):
    """Find the smallest element in a rotated sorted array.

    Distinct values: O(log n).
    Duplicate-heavy input: O(n) worst case.
    """
    if not a:
        raise ValueError("Cannot find a pivot in an empty sequence.")

    lo = 0
    hi = len(a) - 1

    while lo < hi:
        mid = (lo + hi) // 2

        if a[mid] > a[hi]:
            lo = mid + 1
        elif a[mid] < a[hi]:
            hi = mid
        else:
            # Duplicates make the side ambiguous.
            hi -= 1

    return lo


def search_rotated(a, target):
    """Search for target in a rotated sorted array.

    Returns an index or -1.
    Works with duplicate values.
    """
    if not a:
        return -1

    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if a[mid] == target:
            return mid

        if a[lo] < a[mid]:
            # Left side is definitely sorted.
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1

        elif a[lo] > a[mid]:
            # Right side is sorted.
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

        else:
            # Duplicate boundary.
            lo += 1

    return -1


def first_score_at_least(rotated_scores, target):
    """Return original index of the first logical score >= target.

    The input is assumed to be an ascending score list that has been
    rotated. Returns None when no score qualifies.
    """
    if not rotated_scores:
        return None

    pivot = find_pivot(rotated_scores)
    n = len(rotated_scores)

    lo = 0
    hi = n

    # Binary search in logical (unrotated) order.
    while lo < hi:
        mid = (lo + hi) // 2
        value = rotated_scores[(pivot + mid) % n]

        if value < target:
            lo = mid + 1
        else:
            hi = mid

    if lo == n:
        return None

    return (pivot + lo) % n


def feasible(legs, k, capacity):
    """Greedily check whether the route fits into at most k groups."""
    if k <= 0:
        return False

    if not legs:
        return True

    if capacity < max(legs):
        return False

    groups = 1
    used = 0

    for distance in legs:
        if distance > capacity:
            return False

        if used + distance > capacity:
            groups += 1
            used = distance

            if groups > k:
                return False
        else:
            used += distance

    return True


def min_capacity(legs, k):
    """Binary search the smallest capacity that passes feasible()."""
    if not legs:
        return 0

    if k <= 0:
        raise ValueError("k must be positive.")

    if any(distance <= 0 for distance in legs):
        raise ValueError("All route legs must be positive.")

    lo = max(legs)
    hi = sum(legs)

    while lo < hi:
        mid = (lo + hi) // 2

        if feasible(legs, k, mid):
            hi = mid
        else:
            lo = mid + 1

    return lo


def select_best_routes(routes, min_score, k, capacity_limit=None):
    """Return qualifying routes sorted by:
       1. higher score
       2. lower capacity
       3. route ID
    """
    results = []

    for route in routes:
        if route.score < min_score:
            continue

        capacity = min_capacity(route.legs, k)

        if capacity_limit is not None and capacity > capacity_limit:
            continue

        results.append(
            RouteResult(route.route_id, route.score, capacity)
        )

    results.sort(
        key=lambda result: (
            -result.score,
            result.min_capacity,
            result.route_id,
        )
    )

    return results


def highest_feasible_score(routes, k, capacity_limit):
    """Return the highest route score that fits within capacity_limit."""
    scores = []

    for route in routes:
        capacity = min_capacity(route.legs, k)

        if capacity <= capacity_limit:
            scores.append(route.score)

    if not scores:
        return None

    scores.sort()

    # Binary search for the last available score.
    lo = 0
    hi = len(scores)

    while lo < hi:
        mid = (lo + hi) // 2
        lo = mid + 1

    return scores[lo - 1]
