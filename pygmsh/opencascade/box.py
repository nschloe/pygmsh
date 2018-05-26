# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Box(VolumeBase):
    """
    Creates a box.

    Parameters
    ----------
    x0 : array-like[3]
        List containing the x, y, z values of the start point.
    extends : array-like[3]
        List of the 3 extents of the box edges.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

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
