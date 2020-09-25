from math import pi

import gmsh


class Torus:
    """
    Creates a torus.

    center : array-like[3]
        The 3 coordinates of its center.
    radius0 : float
        Inner radius.
    radius1 : float
        Outer radius.
    alpha : float
        Defines the angular opening.
    """

    def __init__(self, center, radius0, radius1, alpha=2 * pi):
        assert len(center) == 3

        self.center = center
        self.radius0 = radius0
        self.radius1 = radius1
        self.alpha = alpha

        self._ID = gmsh.model.occ.addTorus(*center, radius0, radius1, angle=alpha)
        self.dim_tags = [(3, self._ID)]

    def __repr__(self):
        return f"<pygmsh Torus object, ID {self._ID}>"
