"""Selects the appropriate motion controller."""


class MotionController:

    def __init__(
        self,
        straight_controller,
        curve_controller
    ):

        self.straight_controller = (
            straight_controller
        )

        self.curve_controller = (
            curve_controller
        )
