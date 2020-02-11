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
        super().__init__()

        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)

        self.start = start
        self.center = center
        self.end = end

        self.code = "\n".join(
            [
                f"{self.id} = newl;",
                "Circle({}) = {{{}, {}, {}}};".format(
                    self.id, start.id, center.id, end.id
                ),
            ]
        )
        return
