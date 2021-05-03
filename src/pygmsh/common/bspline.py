from .line_base import LineBase
from .point import Point


class BSpline(LineBase):
    """
    Creates a B-spline.

    Parameters
    ----------
    control_points : List[Point]
        Contains the identification numbers of the control points.
    """

    def __init__(self, env, control_points):
        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 1

        id0 = env.addBSpline([c._id for c in control_points])
        super().__init__(id0, control_points)
