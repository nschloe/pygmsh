# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Wedge(VolumeBase):
    def __init__(self, x0, extents, top_extent=None, char_length=None):
        super(Wedge, self).__init__()

        self.x0 = x0
        self.extents = extents
        self.top_extent = top_extent
        self.char_length = char_length

        args = list(x0) + list(extents)
        if top_extent is not None:
            args.append(top_extent)
        args = ', '.join(['{}'.format(arg) for arg in args])

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Wedge({}) = {{{}}};'.format(self.id, args)
            ] + self.char_length_code(char_length)
            )
        return
