# -*- coding: utf-8 -*-
#
from .surface_base import SurfaceBase


class Ball(SurfaceBase):
    def __init__(self, x0, radius):
        super(Ball, self).__init__()

        self.x0 = x0
        self.radius = radius

        args = [x0[0], x0[1], x0[2], radius]
        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Sphere({}) = {{{}}};'.format(self.id, args)
            ])
        return
