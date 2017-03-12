# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase


class CompoundSurface(SurfaceBase):
    def __init__(self, surfaces):
        super(CompoundSurface, self).__init__()

        self.surfaces = surfaces

        self.code = '\n'.join([
            '%s = news;' % self.id,
            'Compound Surface(%s) = {%s};'
            % (self.id, ','.join([s.id for s in surfaces]))
            ])
        return
