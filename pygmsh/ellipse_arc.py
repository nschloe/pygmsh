# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class EllipseArc(LineBase):
    def __init__(self, start, center, point_on_major_axis, end):
        super(EllipseArc, self).__init__()

        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(point_on_major_axis, Point)
        assert isinstance(end, Point)

        self.start = start
        self.center = center
        self.point_on_major_axis = point_on_major_axis
        self.end = end

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Ellipse({}) = {{{}, {}, {}, {}}};'.format(
                self.id, start.id, center.id, point_on_major_axis.id, end.id
            )])
        return
