from __future__ import annotations

from .line_base import LineBase
from .point import Point


class Bezier(LineBase):
    """
    Creates a B-spline.

    Parameters
    ----------
    control_points : Contains the identification numbers of the control points.
    """

    def __init__(self, env, control_points: list[Point]):
        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 1

        id0 = env.addBezier([c._id for c in control_points])
        super().__init__(id0, control_points)
