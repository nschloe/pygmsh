import gmsh


class Rectangle:
    """
    Creates a rectangle.

    x0 : array-like[3]
         The 3 first expressions define the lower-left corner.
    a : float
        Rectangle width.
    b : float
        Rectangle height.
    corner_radius : float
        Defines a radius to round the rectangle corners.
    """

    dim = 2

    def __init__(self, x0, a, b, corner_radius=None):
        assert len(x0) == 3

        self.x0 = x0
        self.a = a
        self.b = b
        self.corner_radius = corner_radius

        if corner_radius is None:
            corner_radius = 0.0

        self._ID = gmsh.model.occ.addRectangle(*x0, a, b, roundedRadius=corner_radius)
        self.dim_tags = [(self.dim, self._ID)]

    def __repr__(self):
        return f"<pygmsh Rectangle object, ID {self._ID}>"
