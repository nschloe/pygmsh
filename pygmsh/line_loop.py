# -*- coding: utf-8 -*-
#


class LineLoop(object):
    _ID = 0

    def __init__(self, lines):
        self.lines = lines

        self.id = 'll%d' % LineLoop._ID
        LineLoop._ID += 1

        self.code = '\n'.join([
            '%s = newll;' % self.id,
            'Line Loop(%s) = {%s};'
            % (self.id, ', '.join([l.id for l in lines]))
            ])
        return
