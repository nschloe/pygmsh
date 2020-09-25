import gmsh

from .point import Point


class Line:
    """
    Creates a straight line segment.

    Parameters
    ----------
    p0 : Object
        Point object that represents the start of the line.
    p1 : Object
        Point object that represents the end of the line.

    Attributes
    ----------
    points : array-like[1][2]
        List containing the begin and end points of the line.
    """

    dimension = 1

    def __init__(self, p0, p1):
        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self._ID = gmsh.model.occ.addLine(p0._ID, p1._ID)
        self.dim_tags = [(1, self._ID)]
        self.points = [p0, p1]

    def __repr__(self):
        pts = ", ".join(str(p._ID) for p in self.points)
        return f"<pygmsh Line object, ID {self._ID}, points ({pts})>"
