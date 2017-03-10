# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase
from .line_loop import LineLoop


class PlaneSurface(SurfaceBase):
    def __init__(self, line_loop, holes=None):
        super(PlaneSurface, self).__init__()

        if holes is None:
            holes = []

        assert isinstance(line_loop, LineLoop)
        for ll in holes:
            assert isinstance(ll, LineLoop)

        self.line_loop = line_loop
        self.holes = holes

        line_loops = [line_loop] + holes
        self.code = '\n'.join([
            '%s = news;' % self.id,
            'Plane Surface(%s) = {%s};'
            % (self.id, ','.join([ll.id for ll in line_loops]))
            ])
        return
