import gmsh

from .line_base import LineBase
from .point import Point


class Bspline(LineBase):
    """
    Creates a BSpline.

    Parameters
    ----------
    control_points : List[Point]
        Contains the identification numbers of the control points.
    """

    def __init__(self, control_points):
        super().__init__()

        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 1

        self.control_points = control_points

        self._ID = gmsh.model.geo.addBSpline([c._ID for c in self.control_points])
