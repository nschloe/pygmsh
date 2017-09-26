# -*- coding: utf-8 -*-
#
from .line_base import LineBase


class CompoundLine(LineBase):
    def __init__(self, lines):
        super(CompoundLine, self).__init__()

        self.lines = lines

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Compound Line({}) = {{{}}};'.format(
                self.id, ','.join([l.id for l in self.lines])
            )])
        return
