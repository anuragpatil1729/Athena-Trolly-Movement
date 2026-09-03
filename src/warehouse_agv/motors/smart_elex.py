"""SmartElex 10D driver abstraction.

Controls a DC motor channel on the SmartElex 10D DC Motor Driver HAT.
Uses BCM GPIO numbering on Raspberry Pi.
"""

from typing import Any, Optional

from warehouse_agv.motors.pwm import PWM, get_gpio_backend


class SmartElex10D:
    """SmartElex 10D single motor channel controller."""

    def __init__(
        self,
        pwm_pin: int,
        dir_pin: int,
        pwm_frequency: int = 1000,
        gpio_backend: Optional[Any] = None,
        inverted: bool = False,
    ):
        if pwm_pin is None or dir_pin is None:
            raise ValueError("Both pwm_pin and dir_pin must be provided.")

        self.pwm_pin = int(pwm_pin)
        self.dir_pin = int(dir_pin)
        self.pwm_frequency = int(pwm_frequency)
        self.inverted = bool(inverted)
        self._gpio = gpio_backend if gpio_backend is not None else get_gpio_backend()

        self._setup_hardware()

    def _setup_hardware(self) -> None:
        """Initialize GPIO pins in BCM mode and prepare PWM controller."""
        if hasattr(self._gpio, "getmode") and self._gpio.getmode() is None:
            self._gpio.setmode(self._gpio.BCM)
        if hasattr(self._gpio, "setwarnings"):
            self._gpio.setwarnings(False)

        # Setup DIR pin as digital output, initially LOW (neutral)
        self._gpio.setup(self.dir_pin, self._gpio.OUT, initial=self._gpio.LOW)

        # Initialize PWM controller
        self.pwm = PWM(
            pin=self.pwm_pin,
            frequency=self.pwm_frequency,
            gpio_backend=self._gpio,
        )
        self.pwm.start(0.0)

    def set_motor(
        self,
        pwm_percent: float,
        direction: int | bool | str = 1,
    ) -> None:
        """Set motor speed and direction.

        :param pwm_percent: PWM duty cycle [0.0 - 100.0]
        :param direction: 1/True/'FORWARD' for forward; 0/-1/False/'REVERSE' for reverse
        """
        clamped_pwm = max(0.0, min(100.0, float(pwm_percent)))

        if clamped_pwm <= 0.0:
            self.stop()
            return

        if isinstance(direction, str):
            is_forward = direction.strip().upper() in ("FORWARD", "FORWARDS", "FWD", "1")
        elif isinstance(direction, (int, float)):
            is_forward = direction > 0
        else:
            is_forward = bool(direction)

        if self.inverted:
            is_forward = not is_forward

        dir_value = self._gpio.HIGH if is_forward else self._gpio.LOW
        self._gpio.output(self.dir_pin, dir_value)
        self.pwm.set_duty_cycle(clamped_pwm)

    def stop(self) -> None:
        """Safely stop motor rotation."""
        if hasattr(self, "pwm") and self.pwm is not None:
            self.pwm.set_duty_cycle(0.0)

    def cleanup(self) -> None:
        """Cleanly release GPIO and PWM resources."""
        self.stop()
        if hasattr(self, "pwm") and self.pwm is not None:
            self.pwm.cleanup()
        if self._gpio is not None and hasattr(self._gpio, "cleanup"):
            try:
                self._gpio.cleanup([self.dir_pin, self.pwm_pin])
            except Exception:
                pass
