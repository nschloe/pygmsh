# -*- coding: utf-8 -*-
#
from .point import Point
import copy


class EllipseArc(object):
    _ELLIPSE_ID = 0

    def __init__(self, points):
        for p in points:
            assert isinstance(p, Point)
        assert len(points) == 4

        self.points = points

        self.id = 'ell%d' % EllipseArc._ELLIPSE_ID
        EllipseArc._ELLIPSE_ID += 1

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Ellipse(%s) = {%s, %s, %s, %s};'
            % (self.id, points[0].id, points[1].id, points[2].id, points[3].id)
            ])
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = '-' + neg_self.id
        return neg_self
