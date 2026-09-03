#!/usr/bin/env python3
"""Hardware test script for Motor 1 (Left Drive Motor) via SmartElex 10D.

This script controls ONLY Motor 1 on the SmartElex 10D DC Motor Driver HAT.
Motor 2 is intentionally kept inactive and untouched.

Connections (BCM numbering):
  Motor 1 PWM = BCM GPIO 12 (Physical Pin 32)
  Motor 1 DIR = BCM GPIO 24 (Physical Pin 18)

Safety:
  - Begins in STOPPED state.
  - Conservative 20.0% PWM duty cycle.
  - try/finally ensures motor is stopped and GPIO resources are released on error or Ctrl+C.
  - Strictly requires a physical Raspberry Pi environment with a supported GPIO backend.
"""

import platform
import sys
import time
from pathlib import Path

# Ensure package modules from src are accessible
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from warehouse_agv.config.loader import load_yaml
from warehouse_agv.motors.motor import SmartElexMotor
from warehouse_agv.motors.pwm import get_gpio_backend
from warehouse_agv.motors.smart_elex import SmartElex10D

# Test parameters
TEST_PWM_DUTY_CYCLE: float = 20.0  # Conservative low PWM duty cycle (20%)
STEP_DURATION: float = 2.0         # 2 seconds per stage


def run_motor_1_test() -> None:
    # 1. Environment & hardware verification
    try:
        gpio_backend = get_gpio_backend()
    except RuntimeError as exc:
        print("=" * 70)
        print("[ERROR] Raspberry Pi hardware GPIO backend is not available.")
        print(f"Details: {exc}")
        print(f"Current System: {platform.system()} ({platform.machine()})")
        print("\nHardware motor control requires:")
        print("  1. Raspberry Pi running Linux (Ubuntu / Raspberry Pi OS)")
        print("  2. SmartElex 10D Motor Driver HAT correctly mounted")
        print("  3. External motor power supply connected to SmartElex")
        print("  4. Supported GPIO backend installed (e.g., 'sudo apt install python3-rpi.gpio' or 'python3-rpi-lgpio')")
        print("\nPhysical motor movement is NOT simulated in development mode.")
        print("=" * 70)
        sys.exit(1)

    # 2. Load motor configuration
    config_path = REPO_ROOT / "config" / "motors.yaml"
    if not config_path.exists():
        print(f"[ERROR] Configuration file not found at {config_path}")
        sys.exit(1)

    motors_cfg = load_yaml(config_path)
    motor_1_cfg = motors_cfg.get("motor_1", {})
    pwm_cfg = motors_cfg.get("pwm", {})

    pwm_pin = motor_1_cfg.get("pwm_pin")
    dir_pin = motor_1_cfg.get("dir_pin")
    frequency = pwm_cfg.get("frequency_hz", 1000)
    inverted = motor_1_cfg.get("inverted", False)

    if pwm_pin is None or dir_pin is None:
        print("[ERROR] Motor 1 pins are not properly defined in motors.yaml")
        sys.exit(1)

    print("Initializing Motor 1...")
    print(f"BCM Pin Mapping: PWM1 = BCM GPIO {pwm_pin} (Pin 32), DIR1 = BCM GPIO {dir_pin} (Pin 18)")
    print(f"PWM Frequency: {frequency} Hz")
    print(f"Testing PWM duty cycle: {TEST_PWM_DUTY_CYCLE}%")
    print("Motor 2 status: INACTIVE (untouched)")

    # 3. Initialize hardware abstractions
    driver = SmartElex10D(
        pwm_pin=pwm_pin,
        dir_pin=dir_pin,
        pwm_frequency=frequency,
        gpio_backend=gpio_backend,
        inverted=inverted,
    )
    motor = SmartElexMotor(driver=driver, max_pwm_percent=100.0)

    try:
        # Step 2: Ensure motor is STOPPED initially
        motor.stop()
        print("Motor 1 STOP")
        time.sleep(STEP_DURATION)

        # Step 4: Rotate Motor 1 FORWARD at conservative low speed
        print("Motor 1 FORWARD")
        driver.set_motor(pwm_percent=TEST_PWM_DUTY_CYCLE, direction=1)
        time.sleep(STEP_DURATION)

        # Step 6: STOP the motor
        motor.stop()
        print("Motor 1 STOP")
        time.sleep(STEP_DURATION)

        # Step 8: Rotate Motor 1 in REVERSE at conservative low speed
        print("Motor 1 REVERSE")
        driver.set_motor(pwm_percent=TEST_PWM_DUTY_CYCLE, direction=0)
        time.sleep(STEP_DURATION)

        # Step 10: STOP the motor
        motor.stop()
        print("Motor 1 STOP")

        print("Test complete")

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] User pressed Ctrl+C. Emergency stop triggered.")
        motor.stop()
    except Exception as exc:
        print(f"\n[ERROR] Unexpected error during motor test: {exc}")
        motor.stop()
        raise
    finally:
        # Step 11: Cleanly release GPIO/PWM resources
        motor.stop()
        driver.cleanup()


if __name__ == "__main__":
    run_motor_1_test()
