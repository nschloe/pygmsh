# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class Bspline(LineBase):
    def __init__(self, control_points):
        super(Bspline, self).__init__()

        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 3

        self.control_points = control_points

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'BSpline(%s) = {%s};' %
            (self.id, ', '.join([c.id for c in self.control_points]))
            ])
        return
