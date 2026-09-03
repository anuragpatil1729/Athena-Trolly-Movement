"""Connection between two warehouse nodes."""

from dataclasses import dataclass


@dataclass
class Edge:

    start_node: int

    end_node: int

    path_segment: object

    cost: float = 0.0
