# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class EllipseArc(LineBase):
    def __init__(self, points):
        super(EllipseArc, self).__init__()

        for p in points:
            assert isinstance(p, Point)
        assert len(points) == 4

        self.points = points

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Ellipse(%s) = {%s, %s, %s, %s};'
            % (self.id, points[0].id, points[1].id, points[2].id, points[3].id)
            ])
        return
