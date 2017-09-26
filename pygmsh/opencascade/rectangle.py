# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase


class Rectangle(SurfaceBase):
    def __init__(self, x0, y0, z0, a, b, corner_radius=None):
        super(Rectangle, self).__init__()

        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.a = a
        self.b = b

        args = [x0, y0, z0, a, b]
        if corner_radius is not None:
            args.append(corner_radius)

        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Rectangle({}) = {{{}}};'.format(self.id, args)
            ])
        return
