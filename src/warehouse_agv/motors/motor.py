"""Generic motor interface."""


class Motor:

    def set_speed(
        self,
        speed
    ):

        raise NotImplementedError

    def stop(self):

        self.set_speed(0.0)
