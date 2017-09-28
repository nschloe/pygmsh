# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Cylinder(VolumeBase):
    def __init__(self, x0, axis, radius, angle=None, char_length=None):
        super(Cylinder, self).__init__()

        assert len(x0) == 3
        assert len(axis) == 3

        self.x0 = x0
        self.axis = axis
        self.radius = radius
        self.angle = angle
        self.char_length = char_length

        args = list(x0) + list(axis) + [radius]
        if angle is not None:
            args.append(angle)
        args = ', '.join(['{}'.format(arg) for arg in args])

        code = [
            '{} = newv;'.format(self.id),
            'Cylinder({}) = {{{}}};'.format(self.id, args)
            ]

        if self.char_length:
            code.extend([
                'pts_{}[] = PointsOf{{Volume{{{}}};}};'.format(
                    self.id, self.id
                    ),
                'Characteristic Length{{pts_{}[]}} = {};'.format(
                    self.id, char_length
                    ),
                ])

        self.code = '\n'.join(code)
        return
