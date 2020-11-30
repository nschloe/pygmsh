from math import pi

import gmsh


class Cone:
    """
    Creates a cone.

    center : array-like[3]
        The 3 coordinates of the center of the first circular face.
    axis : array-like[3]
        The 3 components of the vector defining its axis.
    radius0 : float
        Radius of the first circle.
    radius1 : float
        Radius of the second circle.
    angle : float
        Angular opening of the the Cone.
    """

    dim = 3

    def __init__(self, center, axis, radius0, radius1, angle=2 * pi):
        assert len(center) == 3
        assert len(axis) == 3

        self.center = center
        self.axis = axis
        self.radius0 = radius0
        self.radius1 = radius1

        self._id = gmsh.model.occ.addCone(*center, *axis, radius0, radius1, angle=angle)
        self.dim_tag = (3, self._id)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        return f"<pygmsh Cone object, ID {self._id}>"
