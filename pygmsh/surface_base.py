# -*- coding: utf-8 -*-
#


class SurfaceBase(object):
    _ID = 0
    num_edges = 0

    def __init__(self, num_edges=0, id0=None):
        if id0:
            self.id = id0
        else:
            self.id = 's{}'.format(SurfaceBase._ID)
            SurfaceBase._ID += 1
        self.num_edges = num_edges
        return
