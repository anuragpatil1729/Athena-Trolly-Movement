"""Track progress through a parametric path segment."""


class SegmentTracker:

    def __init__(self):

        self.t = 0.0

    def update(self, t):

        self.t = t

    def reset(self):

        self.t = 0.0
