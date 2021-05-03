import gmsh


class Box:
    """
    Creates a box.

    Parameters
    ----------
    x0 : array-like[3]
        List containing the x, y, z values of the start point.
    extends : array-like[3]
        List of the 3 extents of the box edges.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    dim = 3

    def __init__(self, x0, extents, char_length=None):
        assert len(x0) == 3
        assert len(extents) == 3
        self.x0 = x0
        self.extents = extents
        self._id = gmsh.model.occ.addBox(*x0, *extents)
        self.dim_tag = (3, self._id)
        self.dim_tags = [self.dim_tag]
