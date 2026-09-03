"""Project-specific exceptions."""


class AGVError(Exception):

    pass


class PathError(AGVError):

    pass


class SensorError(AGVError):

    pass


class MotorError(AGVError):

    pass
