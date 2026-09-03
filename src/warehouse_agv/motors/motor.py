"""Generic motor interface and SmartElex implementation."""

from typing import Optional
from warehouse_agv.motors.smart_elex import SmartElex10D


class Motor:
    """Abstract motor interface."""

    def set_speed(
        self,
        speed: float,
    ) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        self.set_speed(0.0)


class SmartElexMotor(Motor):
    """DC Motor controlled via SmartElex 10D driver channel."""

    def __init__(
        self,
        driver: SmartElex10D,
        max_pwm_percent: float = 100.0,
    ):
        self.driver = driver
        self.max_pwm_percent = max(0.0, min(100.0, float(max_pwm_percent)))
        self._current_speed: float = 0.0

    def set_speed(
        self,
        speed: float,
    ) -> None:
        """Set normalized motor speed in range [-1.0, 1.0].

        :param speed: Value between -1.0 (full reverse) and 1.0 (full forward).
                      0.0 stops the motor.
        """
        clamped_speed = max(-1.0, min(1.0, float(speed)))
        self._current_speed = clamped_speed

        if abs(clamped_speed) < 1e-4:
            self.stop()
            return

        direction = 1 if clamped_speed > 0 else 0
        pwm_percent = abs(clamped_speed) * self.max_pwm_percent
        self.driver.set_motor(pwm_percent=pwm_percent, direction=direction)

    def stop(self) -> None:
        """Immediately stop the motor."""
        self._current_speed = 0.0
        self.driver.stop()

    @property
    def current_speed(self) -> float:
        """Return the current normalized speed."""
        return self._current_speed
