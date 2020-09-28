from math import pi

import gmsh


class Cylinder:
    """
    Creates a cylinder.

    Parameters
    ----------
    x0 : array-like[3]
        The 3 coordinates of the center of the first circular face.
    axis : array-like[3]
        The 3 components of the vector defining its axis.
    radius : float
        Radius value of the cylinder.
    angle : float
        Angular opening of the cylinder.
    """

    def __init__(self, x0, axis, radius, angle=2 * pi):
        assert len(x0) == 3
        assert len(axis) == 3

        self.x0 = x0
        self.axis = axis
        self.radius = radius
        self.angle = angle

        self._ID = gmsh.model.occ.addCylinder(*x0, *axis, radius, angle=angle)
        self.dim_tags = [(3, self._ID)]

    def __repr__(self):
        return f"<pygmsh Cylinder object, ID {self._ID}>"
