# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class Line(LineBase):
    def __init__(self, p0, p1):
        super(Line, self).__init__()

        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self.points = [p0, p1]

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Line({}) = {{{}, {}}};'.format(self.id, p0.id, p1.id)
            ])
        return
