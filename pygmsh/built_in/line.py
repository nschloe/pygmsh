from .line_base import LineBase
from .point import Point


class Line(LineBase):
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
        super().__init__()

        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self.points = [p0, p1]

        self.code = "\n".join(
            [f"{self.id} = newl;", f"Line({self.id}) = {{{p0.id}, {p1.id}}};"]
        )
        return
