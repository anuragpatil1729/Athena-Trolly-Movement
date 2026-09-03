"""Route representation."""


class Route:

    def __init__(self, segments=None):

        self.segments = segments or []

    def add_segment(self, segment):

        self.segments.append(segment)
