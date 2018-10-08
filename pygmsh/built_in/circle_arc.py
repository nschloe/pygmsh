# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    """
    Creates a circle arc.

    Parameters
    ----------
    start : array-like[3]
        Coordinates of start point needed to construct circle-arc.
    center : array-like[3]
        Coordinates of center point needed to construct circle-arc.
    end : array-like[3]
        Coordinates of end point needed to construct circle-arc.
    """

    def __init__(self, start, center, end):
        super(CircleArc, self).__init__()

        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)

        self.start = start
        self.center = center
        self.end = end

        self.code = "\n".join(
            [
                "{} = newl;".format(self.id),
                "Circle({}) = {{{}, {}, {}}};".format(
                    self.id, start.id, center.id, end.id
                ),
            ]
        )
        return
