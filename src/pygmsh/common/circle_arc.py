from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    """
    Creates a circle arc.

    Parameters
    ----------
    start : Coordinates of start point needed to construct circle-arc.
    center : Coordinates of center point needed to construct circle-arc.
    end : Coordinates of end point needed to construct circle-arc.
    """

    def __init__(self, env, start: Point, center: Point, end: Point):
        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)
        id0 = env.addCircleArc(start._id, center._id, end._id)
        super().__init__(id0, [start, center, end])
