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

    def __init__(self, start, center, point_on_major_axis, end):
        super().__init__()

        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(point_on_major_axis, Point)
        assert isinstance(end, Point)

        self.start = start
        self.center = center
        self.point_on_major_axis = point_on_major_axis
        self.end = end

        self.code = "\n".join(
            [
                f"{self.id} = newl;",
                "Ellipse({}) = {{{}, {}, {}, {}}};".format(
                    self.id, start.id, center.id, point_on_major_axis.id, end.id
                ),
            ]
        )
        return
