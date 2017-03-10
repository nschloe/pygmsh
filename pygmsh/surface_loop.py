# -*- coding: utf-8 -*-
#


class SurfaceLoop(object):
    _ID = 0

    def __init__(self, surfaces):
        self.surfaces = surfaces

        self.id = 'sl%d' % SurfaceLoop._ID
        SurfaceLoop._ID += 1

        self.code = '\n'.join([
            '%s = news;' % self.id,
            'Surface Loop(%s) = {%s};'
            % (self.id, ','.join([s.id for s in surfaces]))
            ])
        return
