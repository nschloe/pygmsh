# -*- coding: utf-8 -*-
#


class LineBase(object):
    _ID = 0

    def __init__(self, id0=None):
        isinstance(id0, str)
        if id0:
            self.id = id0
        else:
            self.id = 'l{}'.format(LineBase._ID)
            LineBase._ID += 1
        return
