# -*- coding: utf-8 -*-
#
import copy


class LineBase(object):
    _ID = 0

    def __init__(self, id0=None):
        if id0:
            self.id = id0
        else:
            self.id = 'l{}'.format(LineBase._ID)
            LineBase._ID += 1
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = '-' + neg_self.id
        return neg_self
