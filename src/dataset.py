import csv
import random
from typing import List
from .models import Route
from .algorithms import min_capacity


def write_routes_csv(routes, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["route_id", "score", "legs"])
        for route in routes:
            writer.writerow([route.route_id, route.score, ",".join(str(x) for x in route.legs)])


def load_routes_csv(path) -> List[Route]:
    routes = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            legs = [int(x) for x in row["legs"].split(",") if x.strip()]
            routes.append(Route.from_values(row["route_id"], float(row["score"]), legs))
    return routes


def generate_arbitrary_routes(count, seed=2026, min_legs=4, max_legs=12,
                              min_distance=10, max_distance=100):
    rng = random.Random(seed)
    routes = []
    for i in range(count):
        leg_count = rng.randint(min_legs, max_legs)
        legs = tuple(rng.randint(min_distance, max_distance) for _ in range(leg_count))
        score = round(rng.uniform(0.0, 1000.0), 6)
        routes.append(Route.from_values("R{:06d}".format(i + 1), score, legs))
    return routes


def generate_monotonic_routes(count, seed=2026, min_legs=4, max_legs=8,
                              min_distance=10, max_distance=40, k=3):
    rng = random.Random(seed)
    leg_count = rng.randint(min_legs, max_legs)
    base = [rng.randint(min_distance, max_distance) for _ in range(leg_count)]
    routes = []
    for i in range(count):
        scale = i + 1
        legs = tuple(x * scale for x in base)
        cap = min_capacity(legs, k)
        score = float(i + 1)
        routes.append(Route.from_values("M{:06d}".format(i + 1), score, legs))
    return routes


def rotate_routes_by_score(routes, pivot=None):
    ordered = sorted(routes, key=lambda r: (r.score, r.route_id))
    if not ordered:
        return []
    if pivot is None:
        pivot = len(ordered) // 2
    pivot %= len(ordered)
    return ordered[pivot:] + ordered[:pivot]
