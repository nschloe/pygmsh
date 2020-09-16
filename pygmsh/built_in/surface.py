from .line_loop import LineLoop

import gmsh


class Surface:
    """
    Generates a Surface from a LineLoop.

    Parameters
    ----------
    line_loop : Object
        LineLoop object that contains all the Line objects for the loop construction.

    Notes
    -----
    With the built-in kernel, the first line loop should be composed of either three or
    four elementary lines.

    With the built-in kernel, the optional In Sphere argument forces the surface to be a
    spherical patch (the extra parameter gives the identification number of the center
    of the sphere).
    """

    dimension = 2

    def __init__(self, line_loop):
        assert isinstance(line_loop, LineLoop)
        self.line_loop = line_loop
        self.num_edges = len(line_loop)
        self._ID = gmsh.model.geo.addSurfaceFilling([self.line_loop._ID])

    def __repr__(self):
        return f"<pygmsh Surface object, ID {self._ID}>"
