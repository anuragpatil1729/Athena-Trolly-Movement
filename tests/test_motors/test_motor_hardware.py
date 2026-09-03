"""Unit tests for SmartElex 10D, PWM abstraction, and Motor classes.

These tests use a mock GPIO backend and run in any environment (including macOS development machines)
without requiring physical Raspberry Pi hardware.
"""

from pathlib import Path
import pytest

from warehouse_agv.config.loader import load_yaml
from warehouse_agv.motors.motor import SmartElexMotor
from warehouse_agv.motors.pwm import PWM
from warehouse_agv.motors.smart_elex import SmartElex10D


class MockPWMInstance:
    """Mock for GPIO.PWM instance."""

    def __init__(self, pin: int, frequency: int):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0.0
        self.running = False

    def start(self, duty_cycle: float):
        self.duty_cycle = duty_cycle
        self.running = True

    def ChangeDutyCycle(self, duty_cycle: float):
        self.duty_cycle = duty_cycle

    def stop(self):
        self.duty_cycle = 0.0
        self.running = False


class MockGPIO:
    """Mock for Raspberry Pi GPIO module."""

    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    HIGH = 1
    LOW = 0

    def __init__(self):
        self._mode = None
        self._warnings = True
        self.pin_modes = {}
        self.pin_outputs = {}
        self.pwm_instances = {}
        self.cleaned_up_pins = []

    def setmode(self, mode):
        self._mode = mode

    def getmode(self):
        return self._mode

    def setwarnings(self, state):
        self._warnings = state

    def setup(self, pin, mode, initial=None):
        self.pin_modes[pin] = mode
        if initial is not None:
            self.pin_outputs[pin] = initial

    def output(self, pin, value):
        self.pin_outputs[pin] = value

    def PWM(self, pin, frequency):
        mock_pwm = MockPWMInstance(pin, frequency)
        self.pwm_instances[pin] = mock_pwm
        return mock_pwm

    def cleanup(self, pins=None):
        if pins is None:
            self.cleaned_up_pins.append("ALL")
        else:
            self.cleaned_up_pins.extend(pins)


@pytest.fixture
def mock_gpio():
    return MockGPIO()


def test_pwm_initialization_and_duty_cycle(mock_gpio):
    """Verify PWM setup, clamping, and stop."""
    pwm = PWM(pin=12, frequency=1000, gpio_backend=mock_gpio)
    assert mock_gpio.getmode() == mock_gpio.BCM
    assert mock_gpio.pin_modes[12] == mock_gpio.OUT

    pwm.start(10.0)
    assert mock_gpio.pwm_instances[12].duty_cycle == 10.0
    assert mock_gpio.pwm_instances[12].running is True

    # Test duty cycle clamping
    pwm.set_duty_cycle(150.0)
    assert mock_gpio.pwm_instances[12].duty_cycle == 100.0

    pwm.set_duty_cycle(-20.0)
    assert mock_gpio.pwm_instances[12].duty_cycle == 0.0

    pwm.stop()
    assert mock_gpio.pwm_instances[12].running is False


def test_smart_elex_initializes_stopped(mock_gpio):
    """Verify SmartElex 10D starts with DIR LOW and PWM 0%."""
    driver = SmartElex10D(
        pwm_pin=12,
        dir_pin=24,
        pwm_frequency=1000,
        gpio_backend=mock_gpio,
    )
    assert mock_gpio.pin_modes[24] == mock_gpio.OUT
    assert mock_gpio.pin_outputs[24] == mock_gpio.LOW
    assert mock_gpio.pwm_instances[12].duty_cycle == 0.0


def test_smart_elex_forward_and_reverse(mock_gpio):
    """Verify forward sets DIR HIGH and reverse sets DIR LOW."""
    driver = SmartElex10D(
        pwm_pin=12,
        dir_pin=24,
        pwm_frequency=1000,
        gpio_backend=mock_gpio,
    )

    # Forward
    driver.set_motor(pwm_percent=25.0, direction=1)
    assert mock_gpio.pin_outputs[24] == mock_gpio.HIGH
    assert mock_gpio.pwm_instances[12].duty_cycle == 25.0

    # Reverse
    driver.set_motor(pwm_percent=30.0, direction=0)
    assert mock_gpio.pin_outputs[24] == mock_gpio.LOW
    assert mock_gpio.pwm_instances[12].duty_cycle == 30.0

    # Stop
    driver.stop()
    assert mock_gpio.pwm_instances[12].duty_cycle == 0.0


def test_smart_elex_inverted_direction(mock_gpio):
    """Verify direction inversion logic."""
    driver = SmartElex10D(
        pwm_pin=12,
        dir_pin=24,
        pwm_frequency=1000,
        gpio_backend=mock_gpio,
        inverted=True,
    )
    driver.set_motor(pwm_percent=20.0, direction=1)
    assert mock_gpio.pin_outputs[24] == mock_gpio.LOW

    driver.set_motor(pwm_percent=20.0, direction=0)
    assert mock_gpio.pin_outputs[24] == mock_gpio.HIGH


def test_smart_elex_cleanup(mock_gpio):
    """Verify cleanup stops PWM and cleans up pins."""
    driver = SmartElex10D(
        pwm_pin=12,
        dir_pin=24,
        gpio_backend=mock_gpio,
    )
    driver.cleanup()
    assert mock_gpio.pwm_instances[12].running is False
    assert 12 in mock_gpio.cleaned_up_pins
    assert 24 in mock_gpio.cleaned_up_pins


def test_smart_elex_motor_set_speed(mock_gpio):
    """Verify SmartElexMotor wraps normalized speed commands [-1.0, 1.0]."""
    driver = SmartElex10D(
        pwm_pin=12,
        dir_pin=24,
        gpio_backend=mock_gpio,
    )
    motor = SmartElexMotor(driver=driver, max_pwm_percent=100.0)

    # Forward 20%
    motor.set_speed(0.20)
    assert motor.current_speed == 0.20
    assert mock_gpio.pin_outputs[24] == mock_gpio.HIGH
    assert mock_gpio.pwm_instances[12].duty_cycle == 20.0

    # Reverse 30%
    motor.set_speed(-0.30)
    assert motor.current_speed == -0.30
    assert mock_gpio.pin_outputs[24] == mock_gpio.LOW
    assert mock_gpio.pwm_instances[12].duty_cycle == 30.0

    # Stop via set_speed(0.0)
    motor.set_speed(0.0)
    assert motor.current_speed == 0.0
    assert mock_gpio.pwm_instances[12].duty_cycle == 0.0

    # Stop via stop()
    motor.set_speed(0.5)
    motor.stop()
    assert motor.current_speed == 0.0
    assert mock_gpio.pwm_instances[12].duty_cycle == 0.0


def test_config_motor_pins():
    """Verify motors.yaml config: Motor 1 has BCM 12/24, Motor 2 is untouched."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    config_path = repo_root / "config" / "motors.yaml"
    cfg = load_yaml(config_path)

    # Motor 1
    assert cfg["motor_1"]["pwm_pin"] == 12
    assert cfg["motor_1"]["dir_pin"] == 24

    # Motor 2 remains null / untouched
    assert cfg["motor_2"]["pwm_pin"] is None
    assert cfg["motor_2"]["dir_pin"] is None
