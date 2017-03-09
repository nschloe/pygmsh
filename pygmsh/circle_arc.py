# -*- coding: utf-8 -*-
#
from .point import Point


class CircleArc(object):
    _CIRCLE_ID = 0

    def __init__(self, points):
        for p in points:
            assert isinstance(p, Point)

        self.points = points

        self.id = 'c%d' % CircleArc._CIRCLE_ID
        CircleArc._CIRCLE_ID += 1

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Circle(%s) = {%s, %s, %s};'
            % (self.id, points[0].id, points[1].id, points[2].id)
            ])
        return
