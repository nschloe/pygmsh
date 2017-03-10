# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point
import copy


class Line(LineBase):
    def __init__(self, p0, p1):
        super(Line, self).__init__()

        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self.points = [p0, p1]

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Line(%s) = {%s, %s};' % (self.id, p0.id, p1.id)
            ])
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = '-' + neg_self.id
        return neg_self
