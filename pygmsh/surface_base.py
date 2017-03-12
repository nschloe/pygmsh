# -*- coding: utf-8 -*-
#


class SurfaceBase(object):
    _ID = 0

    def __init__(self, id=None):
        if id:
            self.id = id
        else:
            self.id = 's%d' % SurfaceBase._ID
            SurfaceBase._ID += 1
        return
