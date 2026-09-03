"""Combine three deflection measurements."""


def estimate_deflection(
    sensor_angles
):

    if not sensor_angles:

        raise ValueError(
            "No sensor data."
        )

    return sum(
        sensor_angles
    ) / len(
        sensor_angles
    )
