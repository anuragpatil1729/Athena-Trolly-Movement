#!/usr/bin/env python3

import math
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warehouse_agv.simulation.simulated_robot import SimulatedRobot


WHEEL_BASE = 0.60
LEFT_SPEED = 0.50
RIGHT_SPEED = 0.50
TIME_STEP = 0.05
SIMULATION_TIME = 20.0


def update_robot(robot, left_speed, right_speed, dt):
    linear_velocity = (left_speed + right_speed) / 2.0
    angular_velocity = (right_speed - left_speed) / WHEEL_BASE

    robot.x += (
        linear_velocity
        * math.cos(robot.heading)
        * dt
    )

    robot.y += (
        linear_velocity
        * math.sin(robot.heading)
        * dt
    )

    robot.heading += angular_velocity * dt


def run_simulation():
    robot = SimulatedRobot()

    elapsed = 0.0

    trajectory = []

    while elapsed < SIMULATION_TIME:
        update_robot(
            robot,
            LEFT_SPEED,
            RIGHT_SPEED,
            TIME_STEP
        )

        trajectory.append(
            (
                elapsed,
                robot.x,
                robot.y,
                robot.heading
            )
        )

        elapsed += TIME_STEP

    return robot, trajectory


def main():
    robot, trajectory = run_simulation()

    print("Simulation complete")
    print(f"Final X: {robot.x:.3f} m")
    print(f"Final Y: {robot.y:.3f} m")
    print(
        f"Final heading: "
        f"{math.degrees(robot.heading):.2f} deg"
    )

    output_file = PROJECT_ROOT / "data" / "processed" / "simulation.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as file:
        file.write("time,x,y,heading\n")

        for time, x, y, heading in trajectory:
            file.write(
                f"{time:.3f},"
                f"{x:.6f},"
                f"{y:.6f},"
                f"{heading:.6f}\n"
            )

    print(f"Trajectory saved to: {output_file}")


if __name__ == "__main__":
    main()