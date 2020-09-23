import gmsh

from .point import Point


class CircleArc:
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
        self._ID = gmsh.model.occ.addCircleArc(start._ID, center._ID, end._ID)
        self.points = [start, center, end]
