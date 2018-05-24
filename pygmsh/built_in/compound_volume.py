# -*- coding: utf-8 -*-
#


class CompoundVolume(object):
    """
    Generates Compound Volume GMSH function.

    Parameters
    ----------
    volumes : array-like[N]
        Volumes to add to compound volume.
    """

    _ID = 0

    def __init__(self, volumes):
        self.volumes = volumes

        self.id = 'cv{}'.format(CompoundVolume._ID)
        CompoundVolume._ID += 1

        self.code = '\n'.join([
            '{} = newv;'.format(self.id),
            'Compound Volume({}) = {{{}}};'.format(
                self.id, ','.join([v.id for v in volumes])
            )])
        return
