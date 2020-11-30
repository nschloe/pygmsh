from .curve_loop import CurveLoop


class Surface:
    """
    Generates a Surface from a CurveLoop.

    Parameters
    ----------
    curve_loop : Object
        CurveLoop object that contains all the Line objects for the loop construction.

    Notes
    -----
    With the built-in kernel, the first line loop should be composed of either three or
    four elementary lines.

    With the built-in kernel, the optional In Sphere argument forces the surface to be a
    spherical patch (the extra parameter gives the identification number of the center
    of the sphere).
    """

    dim = 2

    def __init__(self, env, curve_loop):
        assert isinstance(curve_loop, CurveLoop)
        self.curve_loop = curve_loop
        self.num_edges = len(curve_loop)
        self._id = env.addSurfaceFilling([self.curve_loop._id])
        self.dim_tag = (2, self._id)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        return f"<pygmsh Surface object, ID {self._id}>"
