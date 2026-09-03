"""
Warehouse AGV main application.

Current architecture:

Warehouse nodes
        ↓
Route planner
        ↓
Parametric path x(t), y(t)
        ↓
Straight / Curve controller
        ↓
Two drive wheel commands
        ↓
SmartElex 10D
        ↓
Two drive motors
"""

from warehouse_agv.robot.robot import Robot


def main():

    print("===================================")
    print(" Warehouse AGV")
    print("===================================")

    robot = Robot()

    robot.start()


if __name__ == "__main__":
    main()
