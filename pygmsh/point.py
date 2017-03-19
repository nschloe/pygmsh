# -*- coding: utf-8 -*-
#


class Point(object):
    _POINT_ID = 0

    def __init__(self, x, lcar):
        self.x = x
        self.lcar = lcar

        self.id = 'p%d' % Point._POINT_ID
        Point._POINT_ID += 1

        self.code = '\n'.join([
            '%s = newp;' % self.id,
            ('Point(%s) = {' +'%r,'*len(x)+'%r};') % (self.id, *x, lcar)
            ])
        return
