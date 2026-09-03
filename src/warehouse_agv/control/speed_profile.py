"""Speed profile for path segments."""


def curve_speed(
    curvature,
    maximum_speed,
    minimum_speed
):

    magnitude = abs(curvature)

    if magnitude <= 0:

        return maximum_speed

    speed = (
        maximum_speed
        /
        (1.0 + magnitude)
    )

    return max(
        minimum_speed,
        speed
    )
