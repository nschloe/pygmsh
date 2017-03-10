# -*- coding: utf-8 -*-
#


class LineBase(object):
    _ID = 0

    def __init__(self, id=None):
        if id:
            self.id = id
        else:
            self.id = 'l%d' % LineBase._ID
            LineBase._ID += 1
        return
