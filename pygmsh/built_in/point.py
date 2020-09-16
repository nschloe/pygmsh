import gmsh

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

    def __init__(self, x, lcar=None):
        super().__init__()

        assert len(x) == 3
        self.x = x
        self.lcar = lcar
        self._ID = gmsh.model.geo.addPoint(x[0], x[1], x[2], meshSize=lcar)
