from .surface_base import SurfaceBase


class CompoundSurface(SurfaceBase):
    """
    Generates the Compound Surface Gmsh function.
    Creates a compound surface from several elementary surfaces.
    When meshed, a compound surface will be reparametrized as
    a single surface, whose mesh can thus cross internal boundaries.
    Compound surfaces are mostly useful for remeshing discrete models.

    Parameters
    ----------
    surfaces : array-like[N]
        Contains the identification number of the elementary surfaces
        that should be reparametrized as a single surface.
    """

    def __init__(self, surfaces):
        super().__init__()
        self.num_edges = sum(s.num_edges for s in surfaces)

        self.surfaces = surfaces

        self.code = "\n".join(
            [
                f"{self.id} = news;",
                "Compound Surface({}) = {{{}}};".format(
                    self.id, ",".join([s.id for s in surfaces])
                ),
            ]
        )
        return
