class Volume:
    """
    Creates a volume.

    Parameters
    ----------
    surface_loop : list
        Contain the identification numbers of all the surface
        loops defining the volume.
    holes : list
        List containing surface loop objects that represents polygon holes.

    Notes
    -----
    The first surface loop defines the exterior boundary of the volume;
    all other surface loops define holes in the volume.

    A surface loop defining a hole should not have any surfaces in common
    with the exterior surface loop (in which case it is not a hole,
    and the two volumes should be defined separately).

    Likewise, a surface loop defining a hole should not have any surfaces
    in common with another surface loop defining a hole in the same volume
    (in which case the two surface loops should be combined).
    """

    dim = 3

    def __init__(self, env, surface_loop, holes=None):
        if holes is None:
            holes = []

        self.surface_loop = surface_loop
        self.holes = holes

        surface_loops = [surface_loop] + holes
        self._id = env.addVolume([s._id for s in surface_loops])
        self.dim_tag = (3, self._id)
        self.dim_tags = [self.dim_tag]
