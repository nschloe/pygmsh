# -*- coding: utf-8 -*-
#


class SurfaceLoop(object):
    """
    Increments the Line ID everytime a new object 
    is created that inherits from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented. 
    """

    _ID = 0
    dimension = 2

    def __init__(self, surfaces):
        self.surfaces = surfaces

        self.id = 'sl{}'.format(SurfaceLoop._ID)
        SurfaceLoop._ID += 1

        self.code = '\n'.join([
            '{} = news;'.format(self.id),
            'Surface Loop({}) = {{{}}};'.format(
                self.id, ','.join([s.id for s in surfaces])
            )])
        return
