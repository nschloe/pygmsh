from .volume_base import VolumeBase


class Torus(VolumeBase):
    """
    Creates a torus.

    center : array-like[3]
        The 3 coordinates of its center.
    radius0 : float
        Inner radius.
    radius1 : float
        Outer radius.
    alpha : float
        Defines the angular opening.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    def __init__(self, center, radius0, radius1, alpha=None, char_length=None):
        super().__init__()

        assert len(center) == 3

        self.center = center
        self.radius0 = radius0
        self.radius1 = radius1
        self.alpha = alpha
        self.char_length = char_length

        args = list(center) + [radius0] + [radius1]
        if alpha is not None:
            args.append(alpha)
        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = newv;", f"Torus({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
