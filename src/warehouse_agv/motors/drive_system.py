"""Two-wheel drive system."""


class DriveSystem:

    def __init__(
        self,
        left_motor,
        right_motor
    ):

        self.left_motor = left_motor

        self.right_motor = right_motor

    def set_wheel_speeds(
        self,
        left,
        right
    ):

        self.left_motor.set_speed(
            left
        )

        self.right_motor.set_speed(
            right
        )

    def stop(self):

        self.left_motor.stop()

        self.right_motor.stop()
