from .curve_loop import CurveLoop


class PlaneSurface:
    """
    Creates a plane surface.

    Parameters
    ----------
    curve_loop : Object
        Each unique line in the line loop will be used
        for the surface construction.
    holes : list
        List of line loops that represents polygon holes.

    Notes
    -----
    The first line loop defines the exterior boundary of the surface;
    all other line loops define holes in the surface.

    A line loop defining a hole should not have any lines in
    common with the exterior line loop (in which case it is not
    a hole, and the two surfaces should be defined separately).

    Likewise, a line loop defining a hole should not have any lines
    in common with another line loop defining a hole in the same
    surface (in which case the two line loops should be combined).
    """

    dim = 2

    def __init__(self, env, curve_loop, holes=None):
        assert isinstance(curve_loop, CurveLoop)
        self.curve_loop = curve_loop

        if holes is None:
            holes = []

        # The input holes are either line loops or entities that contain line loops
        # (like polygons).
        self.holes = [h if isinstance(h, CurveLoop) else h.curve_loop for h in holes]

        self.num_edges = len(self.curve_loop) + sum(len(h) for h in self.holes)

        curve_loops = [self.curve_loop] + self.holes
        self._id = env.addPlaneSurface([ll._id for ll in curve_loops])
        self.dim_tag = (2, self._id)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        return (
            "<pygmsh PlaneSurface object (OCC), "
            f"ID {self._id}, curve loop {self.curve_loop._id}>"
        )
