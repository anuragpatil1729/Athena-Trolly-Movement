"""Sensor health checks."""


def sensor_value_valid(
    value,
    minimum,
    maximum
):

    return (
        minimum <= value <= maximum
    )
