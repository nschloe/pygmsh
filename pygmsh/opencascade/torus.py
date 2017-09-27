# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Torus(VolumeBase):
    def __init__(self, center, radius0, radius1, alpha=None):
        super(Torus, self).__init__()

        assert len(center) == 3

        self.center = center
        self.radius0 = radius0
        self.radius1 = radius1
        self.alpha = alpha

        args = list(center) + [radius0] + [radius1]
        if alpha is not None:
            args.append(alpha)
        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Torus({}) = {{{}}};'.format(self.id, args)
            ])
        return
