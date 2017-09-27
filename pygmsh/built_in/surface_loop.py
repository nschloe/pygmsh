# -*- coding: utf-8 -*-
#


class SurfaceLoop(object):
    _ID = 0

    def __init__(self, surfaces):
        self.surfaces = surfaces

        self.id = 'sl{}'.format(SurfaceLoop._ID)
        SurfaceLoop._ID += 1

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Surface Loop({}) = {{{}}};'.format(
                self.id, ','.join([s.id for s in surfaces])
            )])
        return
