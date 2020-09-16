import gmsh

from .line_base import LineBase
from .point import Point


class Spline(LineBase):
    """
    With the built-in geometry kernel this constructs a Catmull-Rom spline.

    Parameters
    ----------
    points : list
        List containing Point objects
    """

    def __init__(self, points):
        super().__init__()

        for c in points:
            assert isinstance(c, Point)
        assert len(points) > 1

        self.points = points

        self._ID = gmsh.model.geo.addSpline([c._ID for c in self.points])
