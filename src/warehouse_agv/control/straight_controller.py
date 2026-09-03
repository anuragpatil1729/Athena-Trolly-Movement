"""Straight-path deflection controller."""

from warehouse_agv.control.pid import PID


class StraightController:

    def __init__(
        self,
        kp,
        ki,
        kd
    ):

        self.pid = PID(
            kp,
            ki,
            kd
        )

    def update(
        self,
        deflection,
        base_speed,
        dt
    ):

        correction = self.pid.update(
            deflection,
            dt
        )

        left_speed = (
            base_speed -
            correction
        )

        right_speed = (
            base_speed +
            correction
        )

        return (
            left_speed,
            right_speed
        )
