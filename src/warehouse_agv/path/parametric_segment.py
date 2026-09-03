"""One parametric warehouse path segment."""

from dataclasses import dataclass


@dataclass
class ParametricSegment:

    start_node: int | None

    end_node: int | None

    x_equation: str

    y_equation: str

    t_start: float = 0.0

    t_end: float = 1.0
