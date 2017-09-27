# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase


class Disk(SurfaceBase):
    def __init__(self, x0, y0, z0, radius0, radius1=None):
        super(Disk, self).__init__()

        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.radius0 = radius0
        self.radius1 = radius1

        args = [x0, y0, z0, radius0]
        if radius1 is not None:
            args.append(radius1)

        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Disk({}) = {{{}}};'.format(self.id, args)
            ])
        return
