"""Potentiometer calibration and conversion."""


class Potentiometer:

    def __init__(
        self,
        raw_min,
        raw_max,
        angle_min,
        angle_max
    ):

        self.raw_min = raw_min

        self.raw_max = raw_max

        self.angle_min = angle_min

        self.angle_max = angle_max

    def raw_to_angle(self, raw):

        if self.raw_max == self.raw_min:

            raise ValueError(
                "Invalid potentiometer calibration."
            )

        ratio = (
            (raw - self.raw_min)
            /
            (self.raw_max - self.raw_min)
        )

        return (
            self.angle_min
            +
            ratio
            *
            (
                self.angle_max
                -
                self.angle_min
            )
        )
