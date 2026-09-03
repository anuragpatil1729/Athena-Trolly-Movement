"""High-level AGV robot."""

from warehouse_agv.robot.state import (
    RobotState
)


class Robot:

    def __init__(self):

        self.state = RobotState.IDLE

    def start(self):

        print(
            "Robot initialized."
        )

        self.state = (
            RobotState.IDLE
        )

    def stop(self):

        print(
            "Robot stopped."
        )

        self.state = (
            RobotState.STOPPED
        )
