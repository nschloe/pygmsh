# -*- coding: utf-8 -*-
#
from .point import Point
import copy


class Line(object):
    _LINE_ID = 0

    def __init__(self, p0, p1):
        assert isinstance(p0, Point)
        assert isinstance(p1, Point)

        self.points = [p0, p1]

        self.id = 'l%d' % Line._LINE_ID
        Line._LINE_ID += 1

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Line(%s) = {%s, %s};' % (self.id, p0.id, p1.id)
            ])
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = '-' + neg_self.id
        return neg_self
