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
from warehouse_agv.motors.drive_system import DriveSystem


TEST_SPEED = 0.20
TEST_DURATION = 2.0


def load_configuration():

    config_file = PROJECT_ROOT / "config" / "motors.yaml"

    config = load_yaml(config_file)

    motor_1 = config["motor_1"]
    motor_2 = config["motor_2"]
    pwm = config["pwm"]

    required = (
        ("motor_1", motor_1),
        ("motor_2", motor_2),
    )

    for name, motor in required:

        if motor.get("pwm_pin") is None:
            raise RuntimeError(
                f"{name}: pwm_pin is not configured."
            )

        if motor.get("dir_pin") is None:
            raise RuntimeError(
                f"{name}: dir_pin is not configured."
            )

    return motor_1, motor_2, pwm


def create_motor(configuration, pwm_config, gpio):

    driver = SmartElex10D(
        pwm_pin=configuration["pwm_pin"],
        dir_pin=configuration["dir_pin"],
        pwm_frequency=pwm_config["frequency_hz"],
        gpio_backend=gpio,
        inverted=configuration.get(
            "inverted",
            False
        ),
    )

    motor = SmartElexMotor(
        driver=driver,
        max_pwm_percent=configuration.get(
            "max_pwm_percent",
            100
        ),
    )

    return motor, driver


def run_test():

    motor_1_config, motor_2_config, pwm_config = (
        load_configuration()
    )

    gpio = get_gpio_backend()

    left_motor = None
    right_motor = None

    left_driver = None
    right_driver = None

    try:

        left_motor, left_driver = create_motor(
            motor_1_config,
            pwm_config,
            gpio
        )

        right_motor, right_driver = create_motor(
            motor_2_config,
            pwm_config,
            gpio
        )

        drive = DriveSystem(
            left_motor=left_motor,
            right_motor=right_motor
        )

        drive.stop()

        time.sleep(1)

        drive.set_wheel_speeds(
            TEST_SPEED,
            TEST_SPEED
        )

        time.sleep(TEST_DURATION)

        drive.stop()

        time.sleep(1)

        drive.set_wheel_speeds(
            -TEST_SPEED,
            -TEST_SPEED
        )

        time.sleep(TEST_DURATION)

        drive.stop()

        time.sleep(1)

        drive.set_wheel_speeds(
            TEST_SPEED,
            -TEST_SPEED
        )

        time.sleep(TEST_DURATION)

        drive.stop()

        time.sleep(1)

        drive.set_wheel_speeds(
            -TEST_SPEED,
            TEST_SPEED
        )

        time.sleep(TEST_DURATION)

        drive.stop()

    except KeyboardInterrupt:

        if left_motor:
            left_motor.stop()

        if right_motor:
            right_motor.stop()

    finally:

        if left_motor:
            left_motor.stop()

        if right_motor:
            right_motor.stop()

        if left_driver:
            left_driver.cleanup()

        if right_driver:
            right_driver.cleanup()


if __name__ == "__main__":
    run_test()