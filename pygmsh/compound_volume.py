# -*- coding: utf-8 -*-
#


class CompoundVolume(object):
    _ID = 0

    def __init__(self, volumes):
        self.volumes = volumes

        self.id = 'cv%d' % CompoundVolume._ID
        CompoundVolume._ID += 1

        self.code = '\n'.join([
            '%s = newv;' % self.id,
            'Compound Volume(%s) = {%s};'
            % (self.id, ','.join([v.id for v in volumes]))
            ])
        return
