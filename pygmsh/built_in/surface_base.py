# -*- coding: utf-8 -*-
#


class SurfaceBase(object):
    _ID = 0
    num_edges = 0
    dimension = 2

    def __init__(self, id0=None, num_edges=0):
        if id0:
            assert isinstance(id0, str)
            self.id = id0
        else:
            self.id = 's{}'.format(SurfaceBase._ID)
            SurfaceBase._ID += 1
        self.num_edges = num_edges
        return
