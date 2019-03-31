# -*- coding: utf-8 -*-
#
from .point_base import PointBase


class Point(PointBase):
    """
    Creates an elementary point.

    x : array-like[3]
        Give the three X, Y and Z coordinates of the
        point in the three-dimensional Euclidean space.
    lcar : float
        The prescribed mesh element size at this point.
    """

    dimension = 0

    def __init__(self, x, lcar=None):
        super(Point, self).__init__()

        self.x = x
        self.lcar = lcar

        # Points are always 3D in gmsh
        args = (x[0], x[1], x[2]) if lcar is None else (x[0], x[1], x[2], lcar)
        fmt = ", ".join(len(args) * ["{!r}"])

        self.code = "\n".join(
            [
                "{} = newp;".format(self.id),
                ("Point({}) = {{" + fmt + "}};").format(self.id, *args),
            ]
        )
        return
