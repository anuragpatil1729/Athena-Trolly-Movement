#!/usr/bin/env python3

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warehouse_agv.config.loader import load_yaml
from warehouse_agv.motors.motor import SmartElexMotor
from warehouse_agv.motors.pwm import get_gpio_backend
from warehouse_agv.motors.smart_elex import SmartElex10D


STEP_DURATION = 2.0

PWM_LEVELS = (
    10.0,
    15.0,
    20.0,
    25.0,
    30.0,
)


def load_motor_configuration():
    config_file = PROJECT_ROOT / "config" / "motors.yaml"

    config = load_yaml(config_file)

    motor = config["motor_1"]
    pwm = config["pwm"]

    if motor.get("pwm_pin") is None:
        raise RuntimeError(
            "Motor 1 PWM pin is not configured."
        )

    if motor.get("dir_pin") is None:
        raise RuntimeError(
            "Motor 1 DIR pin is not configured."
        )

    return motor, pwm


def create_motor():
    motor_config, pwm_config = load_motor_configuration()

    gpio = get_gpio_backend()

    driver = SmartElex10D(
        pwm_pin=motor_config["pwm_pin"],
        dir_pin=motor_config["dir_pin"],
        pwm_frequency=pwm_config["frequency_hz"],
        gpio_backend=gpio,
        inverted=motor_config.get(
            "inverted",
            False
        ),
    )

    motor = SmartElexMotor(
        driver=driver,
        max_pwm_percent=motor_config.get(
            "max_pwm_percent",
            100
        ),
    )

    return motor, driver


def run_calibration():
    motor, driver = create_motor()

    try:
        motor.stop()

        for pwm in PWM_LEVELS:

            print(
                f"Testing forward at {pwm:.0f}%"
            )

            motor.set_speed(
                pwm / 100.0
            )

            time.sleep(STEP_DURATION)

            motor.stop()

            time.sleep(1.0)

        for pwm in reversed(PWM_LEVELS):

            print(
                f"Testing reverse at {pwm:.0f}%"
            )

            motor.set_speed(
                -(pwm / 100.0)
            )

            time.sleep(STEP_DURATION)

            motor.stop()

            time.sleep(1.0)

        motor.stop()

    except KeyboardInterrupt:

        motor.stop()

    finally:

        motor.stop()
        driver.cleanup()


if __name__ == "__main__":
    run_calibration()