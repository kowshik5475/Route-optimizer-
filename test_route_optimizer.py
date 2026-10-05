"""
Tests for Route / Score Optimizer.
Compatible with Python 3.7+ and Jupyter/Colab.
"""

import random
import unittest

from route_optimizer import (
    Route,
    feasible,
    find_pivot,
    first_score_at_least,
    highest_feasible_score,
    min_capacity,
    search_rotated,
    select_best_routes,
)


def brute_min_capacity(legs, k):
    """Slow reference implementation used to verify binary search."""
    if not legs:
        return 0

    for capacity in range(max(legs), sum(legs) + 1):
        if feasible(legs, k, capacity):
            return capacity

    raise AssertionError("No valid capacity found.")


class TestRotatedSearch(unittest.TestCase):

    def test_rotated_pivot(self):
        self.assertEqual(
            find_pivot([40, 55, 70, 5, 12, 25]),
            3
        )

    def test_sorted_pivot(self):
        self.assertEqual(
            find_pivot([1, 2, 3, 4, 5]),
            0
        )

    def test_duplicate_pivot(self):
        values = [3, 3, 4, 5, 1, 2, 3]
        index = find_pivot(values)
        self.assertEqual(values[index], 1)

    def test_single_value(self):
        self.assertEqual(find_pivot([7]), 0)

    def test_search_existing(self):
        values = [40, 55, 70, 5, 12, 25]
        self.assertNotEqual(search_rotated(values, 12), -1)

    def test_search_missing(self):
        values = [40, 55, 70, 5, 12, 25]
        self.assertEqual(search_rotated(values, 99), -1)

    def test_first_score_at_least(self):
        values = [70, 80, 90, 20, 40, 60]
        index = first_score_at_least(values, 45)
        self.assertEqual(values[index], 60)

    def test_no_score_at_least(self):
        values = [70, 80, 90, 20, 40, 60]
        self.assertIsNone(first_score_at_least(values, 100))


class TestCapacity(unittest.TestCase):

    def test_empty_route(self):
        self.assertEqual(min_capacity([], 3), 0)

    def test_one_group(self):
        self.assertEqual(
            min_capacity([10, 20, 30], 1),
            60
        )

    def test_one_group_per_leg(self):
        self.assertEqual(
            min_capacity([10, 20, 30], 3),
            30
        )

    def test_longest_leg_lower_bound(self):
        self.assertEqual(
            min_capacity([4, 4, 17, 4], 4),
            17
        )

    def test_invalid_k(self):
        with self.assertRaises(ValueError):
            min_capacity([1, 2], 0)

    def test_random_bruteforce(self):
        rng = random.Random(2026)

        for unused in range(300):
            count = rng.randint(1, 7)
            legs = [
                rng.randint(1, 15)
                for unused2 in range(count)
            ]
            k = rng.randint(1, count)

            expected = brute_min_capacity(legs, k)
            actual = min_capacity(legs, k)

            self.assertEqual(
                actual,
                expected,
                "legs={}, k={}".format(legs, k)
            )


class TestRouteSelection(unittest.TestCase):

    def setUp(self):
        self.routes = [
            Route.from_values("R1", 80, [10, 20, 10, 20]),
            Route.from_values("R2", 90, [25, 25, 10]),
            Route.from_values("R3", 90, [15, 15, 15, 15]),
            Route.from_values("R4", 70, [30, 5, 25]),
        ]

    def test_score_capacity_tie_break(self):
        results = select_best_routes(
            self.routes,
            min_score=80,
            k=2
        )

        self.assertEqual(
            [result.route_id for result in results],
            ["R3", "R2", "R1"]
        )

    def test_capacity_filter(self):
        results = select_best_routes(
            self.routes,
            min_score=70,
            k=2,
            capacity_limit=35
        )

        for result in results:
            self.assertLessEqual(result.min_capacity, 35)

    def test_empty_routes(self):
        self.assertEqual(
            select_best_routes([], 50, 2),
            []
        )

    def test_highest_score_under_capacity(self):
        self.assertEqual(
            highest_feasible_score(
                self.routes,
                k=2,
                capacity_limit=35
            ),
            90
        )


def run_tests():
    """Notebook-friendly test runner."""
    suite = unittest.defaultTestLoader.loadTestsFromModule(
        __import__(__name__)
    )

    result = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    unittest.main()
