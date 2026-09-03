"""Parametric curve controller."""

from warehouse_agv.mathematics.wheel_kinematics import (
    wheel_speeds
)


class CurveController:

    def update(
        self,
        linear_velocity,
        curvature,
        wheel_separation
    ):

        angular_velocity = (
            linear_velocity *
            curvature
        )

        return wheel_speeds(
            linear_velocity,
            angular_velocity,
            wheel_separation
        )
