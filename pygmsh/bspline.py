# -*- coding: utf-8 -*-
#
from .point import Point


class Bspline(object):
    _BSPLINE_ID = 0

    def __init__(self, control_points):
        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 3

        self.control_points = control_points

        self.id = 'bspline%d' % Bspline._BSPLINE_ID
        Bspline._BSPLINE_ID += 1

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'BSpline(%s) = {%s};' %
            (self.id, ', '.join([c.id for c in self.control_points]))
            ])
        return
