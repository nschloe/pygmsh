# -*- coding: utf-8 -*-
#


class Point(object):
    _POINT_ID = 0

    def __init__(self, x, lcar):
        self.x = x
        self.lcar = lcar

        self.id = 'p{}'.format(Point._POINT_ID)
        Point._POINT_ID += 1

        # Points are always 3D in gmsh
        self.code = '\n'.join([
            '{} = newp;'.format(self.id),
            'Point({}) = {{{!r}, {!r}, {!r}, {!r}}};'.format(
                self.id, x[0], x[1], x[2], lcar
            )])
        return
