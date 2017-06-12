# -*- coding: utf-8 -*-
#
from .line_loop import LineLoop


class RuledSurface(object):
    _ID = 0
    num_edges = 0

    def __init__(self, line_loop):
        assert isinstance(line_loop, LineLoop)

        self.line_loop = line_loop

        self.id = 'rs{}'.format(RuledSurface._ID)
        RuledSurface._ID += 1

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Ruled Surface({}) = {{{}}};'.format(self.id, self.line_loop.id)
            ])
        self.num_edges = len(line_loop)
        return
