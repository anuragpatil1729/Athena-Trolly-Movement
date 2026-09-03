"""Path geometry calculations."""

import math


def heading_from_derivatives(
    dx,
    dy
):

    return math.atan2(
        dy,
        dx
    )


def path_speed_parameter(
    dx,
    dy
):

    return math.sqrt(
        dx * dx +
        dy * dy
    )
