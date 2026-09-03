"""Robot safety layer."""


class SafetyManager:

    def __init__(self):

        self.emergency_stop_active = False

    def emergency_stop(self):

        self.emergency_stop_active = True

    def reset(self):

        self.emergency_stop_active = False

    def is_safe(self):

        return not self.emergency_stop_active
