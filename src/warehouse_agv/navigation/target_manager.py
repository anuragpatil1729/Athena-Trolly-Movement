"""Target node management."""


class TargetManager:

    def __init__(self):

        self.target_node = None

    def set_target(self, node):

        self.target_node = node

    def get_target(self):

        return self.target_node
