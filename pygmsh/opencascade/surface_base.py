# -*- coding: utf-8 -*-
#
from .. import built_in

class SurfaceBase(built_in.surface_base.SurfaceBase):
    _ID = 0
    dimension = 2

    def __init__(self, is_list=False, id0=None):
        super(SurfaceBase, self).__init__(id0=id0)

        self.is_list = is_list
        if is_list:
            self.id += '[]'
        return

    def char_length_code(self, char_length):
        if char_length is None:
            return []

        return [
            'pts_{}[] = PointsOf{{Surface{{{}}};}};'.format(
                self.id, self.id
                ),
            'Characteristic Length{{pts_{}[]}} = {};'.format(
                self.id, char_length
                ),
            ]
