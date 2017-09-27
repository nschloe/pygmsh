# -*- coding: utf-8 -*-
#


class LineBase(object):
    _ID = 0

    def __init__(self, is_list=False, id0=None):
        isinstance(id0, str)
        self.is_list = is_list
        if id0:
            self.id = id0
        else:
            self.id = 'l{}'.format(LineBase._ID)
            LineBase._ID += 1
        if is_list:
            self.id += '[]'
        return
