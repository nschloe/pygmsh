# -*- coding: utf-8 -*-
#


class Volume(object):
    _ID = 0

    def __init__(self, surface_loop, holes=None):
        if holes is None:
            holes = []

        self.surface_loop = surface_loop
        self.holes = holes

        self.id = 'vol{}'.format(Volume._ID)
        Volume._ID += 1

        surface_loops = [surface_loop] + holes

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Volume({}) = {{{}}};'.format(
                self.id, ', '.join([s.id for s in surface_loops])
            )])
        return
