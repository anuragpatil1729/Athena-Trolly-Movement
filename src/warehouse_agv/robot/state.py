"""Robot state."""


from enum import Enum


class RobotState(Enum):

    IDLE = "IDLE"

    PLANNING = "PLANNING"

    MOVING = "MOVING"

    STOPPED = "STOPPED"

    ERROR = "ERROR"

    EMERGENCY_STOP = "EMERGENCY_STOP"
