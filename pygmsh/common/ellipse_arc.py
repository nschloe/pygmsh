from .line_base import LineBase
from .point import Point


class EllipseArc(LineBase):
    """
    Creates an ellipse arc.

    Parameters
    ----------
    start : Point
        Coordinates of start point needed to construct elliptic arc.
    center : Point
        Coordinates of center point needed to construct elliptic arc.
    point_on_major_axis : Point
        Point on the center axis of ellipse.
    end : Point
        Coordinates of end point needed to construct elliptic arc.
    """

    def __init__(self, env, start, center, point_on_major_axis, end):
        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(point_on_major_axis, Point)
        assert isinstance(end, Point)

        id0 = env.addEllipseArc(start._id, center._id, point_on_major_axis._id, end._id)
        super().__init__(id0, [start, center, end])

        self.points = [start, center, end]
        self.point_on_major_axis = point_on_major_axis

    def __repr__(self):
        pts = ", ".join(str(p._id) for p in self.points)
        return f"<pygmsh EllipseArc object, ID {self._id}, points ({pts})>"
