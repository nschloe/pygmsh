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

        self.code = "\n".join(
            [
                f"{self.id} = newl;",
                "Spline({}) = {{{}}};".format(
                    self.id, ", ".join([c.id for c in self.points])
                ),
            ]
        )
        return
