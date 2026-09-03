"""PWM abstraction for Raspberry Pi motor control."""

from typing import Any, Optional


def get_gpio_backend() -> Any:
    """Detect and return an available Raspberry Pi GPIO backend.

    Attempts standard and modern Raspberry Pi GPIO providers suitable for
    Ubuntu Linux on Raspberry Pi (RPi.GPIO, rpi-lgpio).
    Fails clearly if no hardware GPIO interface is available.
    """
    try:
        import RPi.GPIO as GPIO  # type: ignore
        return GPIO
    except (ImportError, RuntimeError) as exc:
        raise RuntimeError(
            "No usable Raspberry Pi GPIO backend found. Hardware motor control requires "
            "a Raspberry Pi running Linux with a GPIO backend installed "
            "(e.g., 'sudo apt install python3-rpi.gpio' or 'sudo apt install python3-rpi-lgpio'). "
            f"Original error: {exc}"
        ) from exc


class PWM:
    """Hardware PWM controller for a single GPIO pin using BCM numbering."""

    def __init__(
        self,
        pin: int,
        frequency: int = 1000,
        gpio_backend: Optional[Any] = None,
    ):
        self.pin = int(pin)
        self.frequency = int(frequency)
        self._gpio = gpio_backend if gpio_backend is not None else get_gpio_backend()
        self._pwm = None
        self._is_running = False

        self._setup()

    def _setup(self) -> None:
        """Initialize pin as output and configure hardware PWM in BCM mode."""
        if hasattr(self._gpio, "getmode") and self._gpio.getmode() is None:
            self._gpio.setmode(self._gpio.BCM)
        if hasattr(self._gpio, "setwarnings"):
            self._gpio.setwarnings(False)

        self._gpio.setup(self.pin, self._gpio.OUT)
        self._pwm = self._gpio.PWM(self.pin, self.frequency)

    def start(self, duty_cycle: float = 0.0) -> None:
        """Start PWM signal at specified duty cycle [0.0 - 100.0]."""
        duty_cycle = max(0.0, min(100.0, float(duty_cycle)))
        if self._pwm is not None:
            self._pwm.start(duty_cycle)
            self._is_running = True

    def set_duty_cycle(self, duty_cycle: float) -> None:
        """Update PWM duty cycle [0.0 - 100.0]."""
        duty_cycle = max(0.0, min(100.0, float(duty_cycle)))
        if not self._is_running:
            self.start(duty_cycle)
        elif self._pwm is not None:
            self._pwm.ChangeDutyCycle(duty_cycle)

    def stop(self) -> None:
        """Stop PWM output immediately."""
        if self._pwm is not None and self._is_running:
            try:
                self._pwm.ChangeDutyCycle(0.0)
            except Exception:
                pass
            try:
                self._pwm.stop()
            except Exception:
                pass
            self._is_running = False

    def cleanup(self) -> None:
        """Cleanly release PWM and pin resources."""
        self.stop()
