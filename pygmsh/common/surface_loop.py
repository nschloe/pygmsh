class SurfaceLoop:
    """
    Creates a surface loop (a shell).

    Parameters
    ----------
    surfaces : list
        Contain the identification numbers of all the elementary surfaces that
        constitute the surface loop.

    Notes
    -----
    A surface loop must always represent a closed shell, and the elementary surfaces
    should be oriented consistently (using negative identification numbers to specify
    reverse orientation).
    """

    dim = 2

    def __init__(self, env, surfaces):
        self.surfaces = surfaces
        self._id = env.addSurfaceLoop([s._id for s in surfaces])
        self.dim_tag = (2, self._id)
        self.dim_tags = [self.dim_tag]
