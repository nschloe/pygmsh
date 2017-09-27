# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Cylinder(VolumeBase):
    def __init__(self, x0, axis, radius, angle=None):
        super(Cylinder, self).__init__()

        assert len(x0) == 3
        assert len(axis) == 3

        self.x0 = x0
        self.axis = axis
        self.radius = radius
        self.angle = angle

        args = list(x0) + list(axis) + [radius]
        if angle is not None:
            args.append(angle)
        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Cylinder({}) = {{{}}};'.format(self.id, args)
            ])
        return
