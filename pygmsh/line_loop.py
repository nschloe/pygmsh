# -*- coding: utf-8 -*-
#


class LineLoop(object):
    _ID = 0

    def __init__(self, lines):
        self.lines = lines

        self.id = 'll{}'.format(LineLoop._ID)
        LineLoop._ID += 1

        self.code = '\n'.join([
            '{} = newll;'.format(self.id),
            'Line Loop({}) = {{{}}};'.format(
                self.id, ', '.join([l.id for l in lines])
            )])
        return

    def __len__(self):
        return len(self.lines)
