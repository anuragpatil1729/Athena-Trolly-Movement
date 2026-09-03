"""Unit conversion utilities."""

import math


def degrees_to_radians(
    degrees
):

    return (
        degrees *
        math.pi /
        180.0
    )


def radians_to_degrees(
    radians
):

    return (
        radians *
        180.0 /
        math.pi
    )
