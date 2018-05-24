# -*- coding: utf-8 -*-
#
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

    def __init__(self, p0, p1):
        super(Line, self).__init__()

        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self.points = [p0, p1]

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Line({}) = {{{}, {}}};'.format(self.id, p0.id, p1.id)
            ])
        return
