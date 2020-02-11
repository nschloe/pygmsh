from .line_loop import LineLoop
from .surface_base import SurfaceBase


class PlaneSurface(SurfaceBase):
    """
    Creates a plane surface.

    Parameters
    ----------
    line_loop : Object
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

    def __init__(self, line_loop, holes=None):
        super().__init__()

        assert isinstance(line_loop, LineLoop)
        self.line_loop = line_loop

        if holes is None:
            holes = []

        # The input holes are either line loops or entities that contain line
        # loops (like polygons).
        self.holes = [h if isinstance(h, LineLoop) else h.line_loop for h in holes]

        line_loops = [self.line_loop] + self.holes
        self.code = "\n".join(
            [
                f"{self.id} = news;",
                "Plane Surface({}) = {{{}}};".format(
                    self.id, ",".join([ll.id for ll in line_loops])
                ),
            ]
        )
        self.num_edges = len(self.line_loop) + sum(len(h) for h in self.holes)
        return
