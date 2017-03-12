# -*- coding: utf-8 -*-
#
from .line_loop import LineLoop


class RuledSurface(object):
    _ID = 0

    def __init__(self, line_loop):
        assert isinstance(line_loop, LineLoop)

        self.line_loop = line_loop

        self.id = 'rs%d' % RuledSurface._ID
        RuledSurface._ID += 1

        self.code = '\n'.join([
            '%s = news;' % self.id,
            'Ruled Surface(%s) = {%s};' % (self.id, self.line_loop.id)
            ])
        return
