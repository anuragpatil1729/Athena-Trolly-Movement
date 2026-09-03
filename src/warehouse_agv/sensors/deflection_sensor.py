"""Three potentiometer deflection sensor system."""


class DeflectionSensor:

    def __init__(
        self,
        sensors
    ):

        self.sensors = sensors

    def read_deflection(
        self,
        raw_values
    ):

        angles = []

        for sensor, raw in zip(
            self.sensors,
            raw_values
        ):

            angles.append(
                sensor.raw_to_angle(raw)
            )

        return angles
