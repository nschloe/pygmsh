from .volume_base import VolumeBase


class Wedge(VolumeBase):
    """
    Creates a right angular wedge.

    x0 : array-like[3]
        The 3 coordinates of the right-angle point.
    extends : array-like[3]
        List of the 3 extends of the box edges.
    top_extend : float
        Defines the top X extent.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    def __init__(self, x0, extents, top_extent=None, char_length=None):
        super().__init__()

        self.x0 = x0
        self.extents = extents
        self.top_extent = top_extent
        self.char_length = char_length

        args = list(x0) + list(extents)
        if top_extent is not None:
            args.append(top_extent)
        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = newv;", f"Wedge({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
