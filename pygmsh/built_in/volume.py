# -*- coding: utf-8 -*-
#

from .volume_base import VolumeBase

class Volume(VolumeBase):
    def __init__(self, surface_loop, holes=None):
        super(Volume, self).__init__()

        if holes is None:
            holes = []

        self.surface_loop = surface_loop
        self.holes = holes

        surface_loops = [surface_loop] + holes

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Volume({}) = {{{}}};'.format(
                self.id, ', '.join([s.id for s in surface_loops])
            )])
        return
