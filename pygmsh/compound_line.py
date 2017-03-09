# -*- coding: utf-8 -*-
#


class CompoundLine(object):
    _LINE_ID = 0

    def __init__(self, lines):
        self.lines = lines

        self.id = 'cl%d' % CompoundLine._LINE_ID
        CompoundLine._LINE_ID += 1

        self.code = '\n'.join([
            '%s = newl;' % self.id,
            'Compound Line(%s) = {%s};'
            % (self.id, ','.join([l.id for l in self.lines]))
            ])
        return
