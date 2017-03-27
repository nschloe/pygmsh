# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    def __init__(self, circle0, center, circle1):
        super(CircleArc, self).__init__()

        assert isinstance(circle0, Point)
        assert isinstance(center, Point)
        assert isinstance(circle1, Point)

        self.points = points

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Circle(%s) = {%s, %s, %s};'
            % (self.id, circle0.id, center.id, circle1.id)
            ])
        return
