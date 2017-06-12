# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase
from .line_loop import LineLoop


class PlaneSurface(SurfaceBase):
    def __init__(self, line_loop, holes=None):
        super(PlaneSurface, self).__init__()

        assert isinstance(line_loop, LineLoop)
        self.line_loop = line_loop

        if holes is None:
            holes = []

        # The input holes are either line loops or entities that contain line
        # loops (like polygons).
        self.holes = [
            h if isinstance(h, LineLoop) else h.line_loop
            for h in holes
            ]

        line_loops = [self.line_loop] + self.holes
        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Plane Surface({}) = {{{}}};'.format(
                self.id, ','.join([ll.id for ll in line_loops])
            )])
        self.num_edges = len(self.line_loop) + sum(len(h) for h in self.holes)
        return
