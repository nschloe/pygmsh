# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class Spline(LineBase):
    def __init__(self, points):
        super(Spline, self).__init__()

        for c in points:
            assert isinstance(c, Point)
        assert len(points) > 1

        self.points = points

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Spline({}) = {{{}}};'.format(
                self.id, ', '.join([c.id for c in self.points])
            )])
        return
