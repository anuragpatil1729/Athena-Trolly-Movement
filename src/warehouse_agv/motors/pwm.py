"""PWM abstraction."""


class PWM:

    def __init__(
        self,
        pin,
        frequency
    ):

        self.pin = pin

        self.frequency = frequency

    def set_duty_cycle(
        self,
        duty_cycle
    ):

        raise NotImplementedError
