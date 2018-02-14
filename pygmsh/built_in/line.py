# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class Line(LineBase):
    def __init__(self, p0, p1, inside_volume=None):
        super(Line, self).__init__()

        assert isinstance(p0, Point)
        assert isinstance(p1, Point)
        self.points = [p0, p1]

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'Line({}) = {{{}, {}}};'.format(self.id, p0.id, p1.id)
            ])

        if inside_volume:
            given_id = inside_volume.id
            if '[]' in given_id or '()' in given_id:
                name, brackets = given_id[:-2], given_id[-2:]
                # In the following line, we transform name[] to name[#name[]-1]
                # in order to assign only the resulting volume to the given label
                resulting_name = name + brackets[0] + '#' + given_id + '-1' + brackets[1]
            else:
                # if the given identity is not an array, 
                # we just assign the given name with the given label
                resulting_name = given_id
            # the given line is inside a volume
            self.code += '\nLine{{{}}} In Volume{{{}}};'.format(self.id, resulting_name)

        return
