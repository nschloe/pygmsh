# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    def __init__(self, points):
        super(CircleArc, self).__init__()

        for p in points:
            assert isinstance(p, Point)

        self.points = points

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Circle(%s) = {%s, %s, %s};'
            % (self.id, points[0].id, points[1].id, points[2].id)
            ])
        return
