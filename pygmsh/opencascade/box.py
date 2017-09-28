# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Box(VolumeBase):
    def __init__(self, x0, extents, char_length=None):
        super(Box, self).__init__()

        assert len(x0) == 3
        assert len(extents) == 3

        self.x0 = x0
        self.extents = extents
        self.char_length = char_length

        args = list(x0) + list(extents)
        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Box({}) = {{{}}};'.format(self.id, args)
            ] + self.char_length_code(char_length)
            )
        return
