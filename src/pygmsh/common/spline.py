from __future__ import annotations

from .line_base import LineBase
from .point import Point


class Spline(LineBase):
    """
    With the built-in geometry kernel this constructs a Catmull-Rom spline.

    Parameters
    ----------
    points : List containing Point objects
    """

    def __init__(self, env, points: list[Point]):
        for c in points:
            assert isinstance(c, Point)
        assert len(points) > 1

        id0 = env.addSpline([c._id for c in points])
        super().__init__(id0, points)
