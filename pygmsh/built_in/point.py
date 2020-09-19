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

    def __init__(self, x, mesh_size=None):
        assert len(x) == 3
        self.x = x
        args = x
        if mesh_size is not None:
            args += [mesh_size]
        id0 = gmsh.model.geo.addPoint(*args)
        super().__init__(id0)

    def __repr__(self):
        X = ", ".join(str(x) for x in self.x)
        return f"<pygmsh Point object, ID {self._ID}, x = [{X}]>"
