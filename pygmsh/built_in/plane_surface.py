import gmsh

from .curve_loop import CurveLoop
from .surface_base import SurfaceBase


class PlaneSurface(SurfaceBase):
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

    def __init__(self, curve_loop, holes=None):
        assert isinstance(curve_loop, CurveLoop)
        self.curve_loop = curve_loop

        if holes is None:
            holes = []

        # The input holes are either line loops or entities that contain line
        # loops (like polygons).
        self.holes = [h if isinstance(h, CurveLoop) else h.curve_loop for h in holes]

        curve_loops = [self.curve_loop] + self.holes
        id0 = gmsh.model.geo.addPlaneSurface([ll._ID for ll in curve_loops])
        super().__init__(id0)
        self.num_edges = len(self.curve_loop) + sum(len(h) for h in self.holes)

    def __repr__(self):
        return (
            "<pygmsh PlaneSurface object, "
            f"ID {self._ID}, curve loop {self.curve_loop._ID}>"
        )
