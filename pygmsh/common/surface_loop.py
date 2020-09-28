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
        self._ID = env.addSurfaceLoop([s._ID for s in surfaces])
