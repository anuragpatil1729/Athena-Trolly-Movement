"""ADC hardware abstraction."""


class ADC:

    def read(self, channel):

        raise NotImplementedError

    def close(self):

        pass
