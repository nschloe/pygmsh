from .surface_base import SurfaceBase


class Disk(SurfaceBase):
    """
    Creates a disk.

    Parameters
    ----------
    x0 : array-like[3]
        The 3 coordinates of the center of the disk face.
    radius0 : float
        Radius value of the disk.
    radius1 : float
        Radius along Y, leading to an ellipse.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    def __init__(self, x0, radius0, radius1=None, char_length=None):
        super().__init__()

        assert len(x0) == 3
        if radius1 is not None:
            assert radius0 >= radius1

        self.x0 = x0
        self.radius0 = radius0
        self.radius1 = radius1
        self.char_length = char_length

        args = list(x0) + [radius0]
        if radius1 is not None:
            args.append(radius1)

        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = news;", f"Disk({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
