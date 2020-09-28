import gmsh


class Wedge:
    """
    Creates a right angular wedge.

    x0 : array-like[3]
        The 3 coordinates of the right-angle point.
    extends : array-like[3]
        List of the 3 extends of the box edges.
    top_extend : float
        Defines the top X extent.
    """

    def __init__(self, x0, extents, top_extent=None):
        self.x0 = x0
        self.extents = extents
        self.top_extent = top_extent

        self._ID = gmsh.model.occ.addWedge(*x0, *extents, ltx=top_extent)
        self.dim_tags = [(3, self._ID)]

    def __repr__(self):
        return f"<pygmsh Wedge object, ID {self._ID}>"
