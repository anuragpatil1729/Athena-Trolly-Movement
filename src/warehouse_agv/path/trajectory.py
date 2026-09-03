"""Trajectory representation."""


class TrajectoryPoint:

    def __init__(
        self,
        t,
        x,
        y,
        heading,
        curvature,
        speed,
    ):

        self.t = t

        self.x = x

        self.y = y

        self.heading = heading

        self.curvature = curvature

        self.speed = speed
