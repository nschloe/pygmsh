import gmsh

from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    """
    Creates a circle arc.

    Parameters
    ----------
    start : Point
        Coordinates of start point needed to construct circle-arc.
    center : Point
        Coordinates of center point needed to construct circle-arc.
    end : Point
        Coordinates of end point needed to construct circle-arc.
    """

    def __init__(self, start, center, end):
        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)
        id0 = gmsh.model.geo.addCircleArc(start._ID, center._ID, end._ID)
        super().__init__(id0, [start, center, end])
