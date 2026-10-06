import unittest

from src.models import Route
from src.algorithms import (
    find_pivot, search_rotated, first_score_at_least,
    feasible, capacity_lower_bound, min_capacity,
    best_route_within_capacity, best_route_monotonic,
)
from src.dataset import generate_monotonic_routes


class AlgorithmTests(unittest.TestCase):
    def test_find_pivot(self):
        self.assertEqual(find_pivot([4, 5, 6, 1, 2, 3]), 3)

    def test_find_pivot_duplicates(self):
        values = [2, 2, 2, 3, 1, 2]
        self.assertEqual(values[find_pivot(values)], 1)

    def test_search_rotated(self):
        values = [4, 5, 6, 1, 2, 3]
        self.assertEqual(values[search_rotated(values, 2)], 2)

    def test_first_score_at_least(self):
        self.assertEqual(first_score_at_least([1, 3, 5, 7], 4), 2)
        self.assertEqual(first_score_at_least([1, 3, 5, 7], 9), -1)

    def test_feasible(self):
        self.assertTrue(feasible([4, 4, 4], 2, 8))
        self.assertFalse(feasible([4, 4, 4], 2, 7))

    def test_lower_bound(self):
        self.assertEqual(capacity_lower_bound([4, 5, 6], 2), 8)

    def test_min_capacity(self):
        self.assertEqual(min_capacity([4, 4, 4], 2), 8)

    def test_fixed_capacity_selection(self):
        routes = [
            Route.from_values("A", 100, [5, 5, 5]),
            Route.from_values("B", 90, [3, 3, 3]),
            Route.from_values("C", 100, [8, 8]),
        ]
        result = best_route_within_capacity(routes, 2, 10)
        self.assertEqual(result.route_id, "C")

    def test_tie_breaking(self):
        routes = [
            Route.from_values("Z", 100, [4, 4]),
            Route.from_values("A", 100, [3, 3, 3]),
        ]
        result = best_route_within_capacity(routes, 2, 6)
        self.assertEqual(result.route_id, "Z")

    def test_monotonic_binary_search_matches_scan(self):
        routes = generate_monotonic_routes(50, seed=7, k=3)
        capacity = min_capacity(routes[24].legs, 3)
        scan = best_route_within_capacity(routes, 3, capacity)
        binary = best_route_monotonic(routes, 3, capacity)
        self.assertIsNotNone(scan)
        self.assertEqual(scan.route_id, binary.route_id)

    def test_empty(self):
        self.assertIsNone(best_route_within_capacity([], 3, 100))

    def test_invalid_k(self):
        with self.assertRaises(ValueError):
            feasible([1, 2], 0, 5)


if __name__ == "__main__":
    unittest.main()
