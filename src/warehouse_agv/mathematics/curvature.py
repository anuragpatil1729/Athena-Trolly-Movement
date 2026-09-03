"""Curvature of a parametric curve."""


def calculate_curvature(
    dx,
    dy,
    ddx,
    ddy
):

    denominator = (
        dx * dx +
        dy * dy
    ) ** 1.5

    if denominator == 0:

        return 0.0

    numerator = (
        dx * ddy -
        dy * ddx
    )

    return numerator / denominator
