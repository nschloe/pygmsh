# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Cone(VolumeBase):
    def __init__(
            self, center, axis, radius0, radius1, alpha=None,
            char_length=None
            ):
        super(Cone, self).__init__()

        assert len(center) == 3
        assert len(axis) == 3

        self.center = center
        self.axis = axis
        self.radius0 = radius0
        self.radius1 = radius1
        self.char_length = char_length

        args = list(center) + list(axis) + [radius0] + [radius1]
        if alpha is not None:
            args.append(alpha)
        args = ', '.join(['{}'.format(arg) for arg in args])

        code = [
            '{} = newv;'.format(self.id),
            'Cone({}) = {{{}}};'.format(self.id, args)
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
