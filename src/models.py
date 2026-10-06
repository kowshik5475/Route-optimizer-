from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Route:
    route_id: str
    score: float
    legs: Tuple[int, ...]

    @classmethod
    def from_values(cls, route_id: str, score: float, legs):
        values = tuple(int(x) for x in legs)
        if not values:
            raise ValueError("legs must be non-empty")
        if any(x <= 0 for x in values):
            raise ValueError("leg distances must be positive")
        return cls(route_id=str(route_id), score=float(score), legs=values)


@dataclass(frozen=True)
class RouteResult:
    route_id: str
    score: float
    min_capacity: int
