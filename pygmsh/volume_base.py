# -*- coding: utf-8 -*-
#


class VolumeBase(object):
    _ID = 0

    def __init__(self, id=None):
        if id:
            self.id = id
        else:
            self.id = 'v%d' % VolumeBase._ID
            VolumeBase._ID += 1
        return
