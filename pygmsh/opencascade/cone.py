from .volume_base import VolumeBase


class Cone(VolumeBase):
    """
    Creates a cone.

    center : array-like[3]
        The 3 coordinates of the center of the first circular face.
    axis : array-like[3]
        The 3 components of the vector defining its axis.
    radius0 : float
        Radius of the first circle.
    radius1 : float
        Radius of the second circle.
    alpha : float
        Angular opening of the the Cone.
    """

    def __init__(self, center, axis, radius0, radius1, alpha=None, char_length=None):
        super().__init__()

        assert len(center) == 3
        assert len(axis) == 3

        self.center = center
        self.axis = axis
        self.radius0 = radius0
        self.radius1 = radius1
        self.char_length = char_length

        args = list(center) + list(axis) + [radius0] + [radius1]
        if alpha is not None:
            args.append(alpha)
        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = newv;", f"Cone({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
