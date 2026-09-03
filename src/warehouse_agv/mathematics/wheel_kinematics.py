"""Two-wheel drive kinematics."""


def wheel_speeds(
    linear_velocity,
    angular_velocity,
    wheel_separation
):

    left = (
        linear_velocity
        -
        (wheel_separation / 2.0)
        * angular_velocity
    )

    right = (
        linear_velocity
        +
        (wheel_separation / 2.0)
        * angular_velocity
    )

    return left, right
