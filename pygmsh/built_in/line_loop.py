# -*- coding: utf-8 -*-
#


class LineLoop(object):
    """
    Increments the Line ID every time a new object is created that inherits
    from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    lines : list
        Contain the identification numbers of all the line loops
        defining the volume.

    Notes
    -----
    A line loop must be a closed loop, and the elementary lines
    should be ordered and oriented (using negative identification
    numbers to specify reverse orientation). If the orientation is
    correct, but the ordering is wrong, Gmsh will actually
    reorder the list internally to create a consistent loop.
    """

    _ID = 0
    dimension = 1

    def __init__(self, lines):
        self.lines = lines

        self.id = "ll{}".format(LineLoop._ID)
        LineLoop._ID += 1

        self.code = "\n".join(
            [
                "{} = newll;".format(self.id),
                "Line Loop({}) = {{{}}};".format(
                    self.id, ", ".join([l.id for l in lines])
                ),
            ]
        )
        return

    def __len__(self):
        return len(self.lines)
