"""
CLI demo.
Works with Python 3.7+.

Windows CMD:
    python main.py

Jupyter/Colab:
    !python main.py
"""

import argparse

from route_optimizer import (
    Route,
    first_score_at_least,
    select_best_routes,
)


ROUTES = [
    Route.from_values("R101", 72, [12, 18, 9, 21, 10]),
    Route.from_values("R102", 88, [20, 15, 25, 10]),
    Route.from_values("R103", 88, [14, 14, 14, 14, 12]),
    Route.from_values("R104", 95, [30, 10, 20, 15]),
    Route.from_values("R105", 81, [11, 19, 13, 17, 8]),
]


def main():
    parser = argparse.ArgumentParser(
        description="Binary-search Route / Score Optimizer"
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=80,
        help="minimum score"
    )

    parser.add_argument(
        "--legs",
        type=int,
        default=3,
        help="maximum number of groups"
    )

    parser.add_argument(
        "--capacity-limit",
        type=int,
        default=None,
        help="optional maximum capacity"
    )

    args = parser.parse_args()

    print("=== Route / Score Optimizer ===")
    print("Minimum score:", args.min_score)
    print("Maximum legs: ", args.legs)

    if args.capacity_limit is not None:
        print("Capacity cap: ", args.capacity_limit)

    print()

    # Demonstrate rotated score searching.
    sorted_scores = sorted(
        route.score for route in ROUTES
    )

    pivot = len(sorted_scores) // 2

    rotated_scores = (
        sorted_scores[pivot:]
        + sorted_scores[:pivot]
    )

    index = first_score_at_least(
        rotated_scores,
        args.min_score
    )

    print("Rotated scores:", rotated_scores)

    if index is None:
        print("No score reaches the requested threshold.")
    else:
        print(
            "First score >= threshold:",
            rotated_scores[index]
        )

    print()

    results = select_best_routes(
        ROUTES,
        args.min_score,
        args.legs,
        args.capacity_limit
    )

    if not results:
        print("No route satisfies the constraints.")
        return

    print(
        "{:<6}{:<10}{:<10}{}".format(
            "Rank",
            "Route",
            "Score",
            "Min capacity"
        )
    )

    print("-" * 41)

    for rank, result in enumerate(results, 1):
        print(
            "{:<6}{:<10}{:<10}{}".format(
                rank,
                result.route_id,
                result.score,
                result.min_capacity
            )
        )

    winner = results[0]

    print()
    print(
        "Winner: {} (score={}, min_capacity={})".format(
            winner.route_id,
            winner.score,
            winner.min_capacity
        )
    )


if __name__ == "__main__":
    main()
