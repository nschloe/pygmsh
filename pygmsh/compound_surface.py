# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase


class CompoundSurface(SurfaceBase):
    def __init__(self, surfaces):
        super(CompoundSurface, self).__init__()
        self.num_edges = sum(s.num_edges for s in surfaces)

        self.surfaces = surfaces

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Compound Surface({}) = {{{}}};'.format(
                self.id, ','.join([s.id for s in surfaces])
            )])
        return
