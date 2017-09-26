# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class CircleArc(LineBase):
    def __init__(self, start, center, end):
        super(CircleArc, self).__init__()

        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)

        self.start = start
        self.center = center
        self.end = end

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Circle({}) = {{{}, {}, {}}};'.format(
                self.id, start.id, center.id, end.id
            )])
        return
