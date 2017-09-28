# -*- coding: utf-8 -*-
#


class VolumeBase(object):
    _ID = 0

    def __init__(self, is_list=False, id0=None):
        isinstance(id0, str)
        self.is_list = is_list
        if id0:
            self.id = id0
        else:
            self.id = 'v{}'.format(VolumeBase._ID)
            VolumeBase._ID += 1
        if is_list:
            self.id += '[]'
        return

    def char_length_code(self, char_length):
        if char_length is None:
            return []

        return [
            'pts_{}[] = PointsOf{{Volume{{{}}};}};'.format(
                self.id, self.id
                ),
            'Characteristic Length{{pts_{}[]}} = {};'.format(
                self.id, char_length
                ),
            ]
