# -*- coding: utf-8 -*-
#
import copy


class LineBase(object):
    _ID = 0

    def __init__(self, id=None):
        if id:
            self.id = id
        else:
            self.id = 'l%d' % LineBase._ID
            LineBase._ID += 1
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = '-' + neg_self.id
        return neg_self
