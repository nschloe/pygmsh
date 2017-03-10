# -*- coding: utf-8 -*-
#
from .line_loop import LineLoop


class PlaneSurface(object):
    _ID = 0

    def __init__(self, line_loop, holes=None):
        if holes is None:
            holes = []

        assert isinstance(line_loop, LineLoop)
        for ll in holes:
            assert isinstance(ll, LineLoop)

        self.id = 'ps%d' % PlaneSurface._ID
        PlaneSurface._ID += 1

        self.line_loop = line_loop
        self.holes = holes

        line_loops = [line_loop] + holes
        self.code = '\n'.join([
            '%s = news;' % self.id,
            'Plane Surface(%s) = {%s};'
            % (self.id, ','.join([ll.id for ll in line_loops]))
            ])
        return
