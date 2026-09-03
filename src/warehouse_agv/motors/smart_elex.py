"""SmartElex 10D driver abstraction.

Hardware GPIO implementation will be connected after the
Raspberry Pi GPIO configuration is finalized.
"""


class SmartElex10D:

    def __init__(
        self,
        pwm_pin,
        dir_pin,
        pwm_frequency=1000
    ):

        self.pwm_pin = pwm_pin

        self.dir_pin = dir_pin

        self.pwm_frequency = (
            pwm_frequency
        )

    def set_motor(
        self,
        pwm_percent,
        direction
    ):

        raise NotImplementedError(
            "GPIO implementation pending."
        )

    def stop(self):

        pass
