# -*- coding: utf-8 -*-
#
from .line_loop import LineLoop


class Surface(object):
    _ID = 0
    num_edges = 0

    def __init__(self, line_loop, api_level=2):
        assert isinstance(line_loop, LineLoop)

        self.line_loop = line_loop

        self.id = 'rs{}'.format(Surface._ID)
        Surface._ID += 1

        # `Ruled Surface` was deprecated in Gmsh 3 in favor of `Surface`.
        name = 'Surface' if api_level > 2 else 'Ruled Surface'

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            '{}({}) = {{{}}};'.format(name, self.id, self.line_loop.id)
            ])
        self.num_edges = len(line_loop)
        return
