"""Track current warehouse node."""


class NodeTracker:

    def __init__(self):

        self.current_node = None

    def set_node(self, node):

        self.current_node = node

    def get_node(self):

        return self.current_node
